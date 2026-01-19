#### 不要存在多余的空格

#### ReadContext方法

- 查询方法的命名为resource{ResourceName}Read，如resourceAppServerGroupScalingPolicyRead，注意不要包含包名。
- 查询方法的入参包含ctx context.Context, d *schema.ResourceData, meta interface{}，ctx为上下文，d为资源数据，meta为元数据。
- 查询方法的返回值为diag.Diagnostics，如果返回diag.Diagnostics类型的错误，则表示创建失败。
- 查询方法的实现步骤为：（其中a,b,d,e步骤与CreateContext保持一致）
    * 获取region。
    * 创建client。
    * 构建请求方法（可能存在额外的请求头、请求体配置处理）。
    * 调用请求方法发送请求。
	* 如返回错误则使用common.CheckDeletedDiag方法判断是否是资源不存在导致的（404错误）
    * 根据查询返回信息回填属性。

##### 构建请求方法

- 如查询请求API为查询列表接口且包含分页查询参数，则需要遵守以下不同分页类型的设计要求：

###### limit+offset

- 通过查询对象列表接口设计而成的复数查询方法，其命名格式为：`list{ObjectName的复数表达}`，入参通常为 `(client *golangsdk.ServiceClient, d *schema.ResourceData)`，出参为`([]interface{}, error)`
- 除了根据URI设置httpUrl外，还需要预置limit（取用API所声明的最大值，如果没声明则默认为100）和offset
- 如果存在query参数，则需要为所有的query参数构造一个build方法，其方法命名格式为：build{ResourceName的复数表达}QueryParams
- 获取本次查询返回的单页对象后将所有值存储于返回的结果列表中并判断本页的对象查询数是否少于limit，如是则立刻返回列表信息（说明已经查询到了最后一页）
- 在未获取至最后一页前不断对offset进行累加（累加值来自当前页查询的对象数，通过len()方法获取
- 查询接口返回的错误不在该方法中格式化

```go
func listComponents(client *golangsdk.ServiceClient) ([]interface{}, error) {
	var (
		httpUrl = "v3/{project_id}/cas/components?limit={limit}"
		limit   = 100
		offset  = 0
		result  = make([]interface{}, 0)
	)

	listPath := client.Endpoint + httpUrl
	listPath = strings.ReplaceAll(listPath, "{project_id}", client.ProjectID)
	listPath = strings.ReplaceAll(listPath, "{limit}", strconv.Itoa(limit))

	opt := golangsdk.RequestOpts{
		KeepResponseBody: true,
		MoreHeaders: map[string]string{
			"Content-Type": "application/json",
		},
	}

	for {
		listPathWithOffset := listPath + fmt.Sprintf("&offset=%d", offset)
		requestResp, err := client.Request("GET", listPathWithOffset, &opt)
		if err != nil {
			return nil, err
		}
		respBody, err := utils.FlattenResponse(requestResp)
		if err != nil {
			return nil, err
		}
		components := utils.PathSearch("components", respBody, make([]interface{}, 0)).([]interface{})
		result = append(result, components...)
		if len(components) < limit {
			break
		}
		offset += len(components)
	}

	return result, nil
}
```

###### marker+maxitems

- 通过查询对象列表接口设计而成的复数查询方法，其命名格式为：`list{ObjectName的复数表达}`，入参通常为`(client *golangsdk.ServiceClient, d *schema.ResourceData)`，出参为`([]interface{}, error)`
- 除了根据URI设置httpUrl外，还需要预置maxitems（取用API所声明的最大值，如果没声明则默认为100）和marker（初始值为0）
- 如果存在query参数，则需要为所有的query参数构造一个build方法，其方法命名格式为：build{ResourceName的复数表达}QueryParams
- 获取本次查询返回的单页对象后将所有值存储于返回的结果列表中并判断返回的下一次查询位置是否等于当前marker或等于零值，如是则立刻返回列表信息（说明已经查询到了最后一页）
- 在未获取至最后一页前持续使用next_marker信息更新下一次查询的marker
- 查询接口返回的错误不在该方法中格式化

```go
func listFunctions(client *golangsdk.ServiceClient, d *schema.ResourceData) ([]interface{}, error) {
	var (
		httpUrl = "v2/{project_id}/fgs/functions?maxitems=100"
		marker  float64
		result  = make([]interface{}, 0)
	)

	listPath := client.Endpoint + httpUrl
	listPath = strings.ReplaceAll(listPath, "{project_id}", client.ProjectID)
	listPath += buildFunctionsQueryParams(d)
	listOpt := golangsdk.RequestOpts{
		KeepResponseBody: true,
		MoreHeaders: map[string]string{
			"Content-Type": "application/json",
		},
	}

	for {
		listPathWithMarker := fmt.Sprintf("%s&marker=%v", listPath, marker)
		requestResp, err := client.Request("GET", listPathWithMarker, &listOpt)
		if err != nil {
			return nil, err
		}
		respBody, err := utils.FlattenResponse(requestResp)
		if err != nil {
			return nil, err
		}
		functions := utils.PathSearch("functions", respBody, make([]interface{}, 0)).([]interface{})
		if len(functions) < 1 {
			break
		}
		result = append(result, functions...)
		// In this API, marker has the same meaning as offset.
		nextMarker := utils.PathSearch("next_marker", respBody, float64(0)).(float64)
		if nextMarker == marker || nextMarker == 0 {
			// Make sure the next marker value is correct, not the previous marker or zero (in the last page).
			break
		}
		marker = nextMarker
	}

	return result, nil
}
```

- 资源中多数使用的是单数对象查询的接口，通常遵循以下设计规则：
- 通过查询对象详情接口设计而成的单数查询方法，其命名格式为：`get{ObjectName}`，入参通常为
  `(client *golangsdk.ServiceClient, resourceId string)`（方法入参的字符串输入可能还包括父资源ID、类型等），出参为`(interface{}, error)`
- 查询接口返回的错误不在该方法中格式化

```go
func GetTrigger(client *golangsdk.ServiceClient, functionUrn, triggerType, triggerId string) (interface{}, error) {
	var (
		httpUrl = "v2/{project_id}/fgs/triggers/{function_urn}/{trigger_type_code}/{trigger_id}"
	)

	getPath := client.Endpoint + httpUrl
	getPath = strings.ReplaceAll(getPath, "{project_id}", client.ProjectID)
	getPath = strings.ReplaceAll(getPath, "{function_urn}", functionUrn)
	getPath = strings.ReplaceAll(getPath, "{trigger_type_code}", triggerType)
	getPath = strings.ReplaceAll(getPath, "{trigger_id}", triggerId)
	getOpts := golangsdk.RequestOpts{
		KeepResponseBody: true,
		MoreHeaders: map[string]string{
			"Content-Type": "application/json",
		},
	}

	requestResp, err := client.Request("GET", getPath, &getOpts)
	if err != nil {
		return nil, err
	}
	return utils.FlattenResponse(requestResp)
}
```

##### CheckDeleted处理

- 对于资源而言，如果在刷新阶段识别到该资源已经不存在了，则需要将该资源的ID置空。
- 该动作通过公共包（common）中的`CheckDeletedDiag()`方法判断查询请求是否出错且错误内容为资源不存在。
- 对于标准的404错误，按照以下格式进行处理

```go
func resourceLifecycleHookRead(_ context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	...

	hook, err := GetLifecycleHook(client, groupId, d.Id())
	if err != nil {
		return common.CheckDeletedDiag(d, err, "error retrieve the lifecycle hook of the autoscaling service")
	}

	...
}
```

- 如果错误信息是非标准404状态码对应的错误则需要通过公共包（common）下的`ConvertExpected400ErrInto404Err()`等方法将非标资源不存在错误（例如400错误）转换成标准的404错误。

```go
func resourceLifecycleHookRead(_ context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	...

	hook, err := GetLifecycleHook(client, groupId, d.Id())
	if err != nil {
		// When querying the lifecycle hook details, if the group does not exist, the following error will be reported:
		// {"error": {"code": "AS.2007","message": "The AS group does not exist."}}.
		// If the hook name does not exist, the response HTTP status code of the details API is 404.
		return common.CheckDeletedDiag(d, common.ConvertExpected400ErrInto404Err(err, "error.code", "AS.2007"),
			"error getting the specifies lifecycle hook of the autoscaling service")
	}

	...
}
```

- 其中各ConvertExpectedErr方法均支持匹配多个错误码，如：

```go
var componentNotFoundCodes = []string{
	"XXX.1001"
	"XXX.1002"
}

func resourceComponentRead(_ context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	...

	getComponentResp, err := getComponent(client, componentId)
	if err != nil {
		return common.CheckDeletedDiag(d, common.ConvertExpected400ErrInto404Err(err, "error_code", componentNotFoundCodes...),
			"error retrieving XXX component")
	}

	...
}
```

- 部分资源可能涉及多种非标404状态码的错误都指向资源不存在，这类资源可以通过各类型ConvertExpectedErr方法之间嵌套实现全错误覆盖：

```go
func resourceComponentRead(_ context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	...

	getComponentResp, err := getComponent(client, componentId)
	if err != nil {
		return common.CheckDeletedDiag(d, common.ConvertExpected400ErrInto404Err(
				common.ConvertExpected403ErrInto404Err(err, "error_code", "XXX.1001"),
				"error_code",
				"XXX.1002",
			), "error retrieving XXX component")
	}

	...
}

common.ConvertExpected401ErrInto404Err(err, "error_code", "DWS.0047")
```

##### 根据查询返回信息回填属性

- 根据查询请求返回的（经过解析的）response body，通过d.Set方法将其所有参数属性逐一进行回填（废弃参数除外，另外region直接通过回填变量）。
- 所有对象（object）类型、列表类型的返回参数或属性必须定义对应的解析方法，其名称格式为：`flatten{ResourceName}{ObjectParamName/ListParamName}`，注意不要包含包名。
- 如果是子参数的解析方法（对象（object）类型、列表类型），则对应嵌套定义出对应的flatten方法，其命名格式为：`flatten{ParentParamName}{ObjectParamName/ListParamName}`。
- object类型的入参固定为`map[string]interface{}`，返回为`[]map[string]interface{}`
- 列表类型的入参固定为`[]interface{}`，返回为`[]map[string]interface{}`
- 参数属性回填时的顺序参考schema的定义顺序并且标识分类，如必选参数，可选参数。
- 所有方法的定义按照递归的格式排列于主方法之上（子方法在父方法之上，父方法下的所有子方法间按照引用顺序排列）

```go
// 注意解析方法的输入：对象类型要求输入map[string]interface{}类型的待解析对象，返回由于Terraform仅支持对象列表故返回[]map[string]interface{}
func flattenScalingPolicyScalingPolicyBySession(scalingPolicyBySession map[string]interface{}) ([]map[string]interface{}) {
	if len(scalingPolicyBySession) < 1 {
		return nil
	}

	return []map[string]interface{}{
		{
			"session_usage_threshold":           utils.PathSearch("session_usage_threshold", scalingPolicyBySession, nil),
			"shrink_after_session_idle_minutes": utils.PathSearch("shrink_after_session_idle_minutes", scalingPolicyBySession, nil),
		}
	}
}

// 注意解析方法的输入：对象类型要求输入map[string]interface{}类型的待解析对象，返回由于Terraform仅支持对象列表故返回[]map[string]interface{}
func flattenScalingPolicyStrategy(strategy map[string]interface{}) ([]map[string]interface{}) {
	if len(strategy) < 1 {
		return nil
	}

	return []map[string]interface{}{
		{
			"type":            utils.PathSearch("type", strategy, nil),
			"rolling_release": utils.JsonToString(utils.PathSearch("rolling_release", strategy, nil)), // 该参数返回为object类型但schema中定义为了JSON string
			"gray_release":    utils.JsonToString(utils.PathSearch("gray_release", strategy, nil)), // 该参数返回为object类型但schema中定义为了JSON string
		}
	}
}

// 注意解析方法的输入：对象列表类型要求输入[]interface{}类型的待解析对象，返回由于Terraform仅支持对象列表故返回[]map[string]interface{}
func flattenScalingPolicyStorages(storage []interface{}) ([]map[string]interface{}) {
	if len(probes) < 1 {
		return nil
	}

	result := make([]map[string]interface{}, 0, len(probes))
	for _, probe := range probes {
		result = append(result, map[string]interface{}{
			"type":    utils.PathSearch("type", probe, nil),
			"delay":   utils.PathSearch("delay", probe, nil),
			"timeout": utils.PathSearch("timeout", probe, nil),
			"scheme":  utils.PathSearch("scheme", probe, nil),
			"host":    utils.PathSearch("host", probe, nil),
			"port":    utils.PathSearch("port", probe, nil),
			"path":    utils.PathSearch("path", probe, nil),
			"command": utils.PathSearch("command", probe, make([]interface{}, 0)),
		})
	}
	return result
}

// 注意解析方法的输入：对象列表类型要求输入[]interface{}类型的待解析对象，返回由于Terraform仅支持对象列表故返回[]map[string]interface{}
func flattenScalingPolicyProbes(probes []interface{}) ([]map[string]interface{}) {
	if len(probes) < 1 {
		return nil
	}

	result := make([]map[string]interface{}, 0, len(probes))
	for _, probe := range probes {
		result = append(result, map[string]interface{}{
			"type":    utils.PathSearch("type", probe, nil),
			"delay":   utils.PathSearch("delay", probe, nil),
			"timeout": utils.PathSearch("timeout", probe, nil),
			"scheme":  utils.PathSearch("scheme", probe, nil),
			"host":    utils.PathSearch("host", probe, nil),
			"port":    utils.PathSearch("port", probe, nil),
			"path":    utils.PathSearch("path", probe, nil),
			"command": utils.PathSearch("command", probe, make([]interface{}, 0)),
		})
	}
	return result
}

func resourceAppServerGroupScalingPolicyRead(ctx context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	...

	mErr := multierror.Append(nil,
		d.Set("region", region), // 项目级资源必须回填
		// Required parameters.
		d.Set("enable", utils.PathSearch("enable", respBody, nil)),
		d.Set("max_scaling_amount", utils.PathSearch("max_scaling_amount", respBody, nil)),
		d.Set("single_expansion_count", utils.PathSearch("single_expansion_count", respBody, nil)),
		d.Set("scaling_policy_by_session", flattenScalingPolicyScalingPolicyBySession(utils.PathSearch("scaling_policy_by_session", respBody,
			make(map[string]interface{})).(map[string]interface{}))),
		// Optional parameters.
		d.Set("server_group_id", utils.PathSearch("server_group_id", respBody, nil)),
		d.Set("ip_addresses", utils.PathSearch("ip_addresses", respBody, nil)),
		d.Set("dns_list", utils.PathSearch("dns_list", respBody, nil)),
		d.Set("strategy", flattenScalingPolicyStrategy(utils.PathSearch("strategy", respBody,
			make(map[string]interface{})).(map[string]interface{}))), // 对象类型的返回在传入解析方法前需要进行断言（注意提供对应类型的默认值）
		d.Set("storages", flattenScalingPolicyStorages(utils.PathSearch("storages", respBody,
			make([]interface{}, 0)).([]interface{}))), // 列表类型的返回在传入解析方法前需要进行断言（注意提供对应类型的默认值），针对TypeSet类型的schema字段无需特殊处理成Set
		d.Set("probes", flattenScalingPolicyProbes(utils.PathSearch("probes", respBody,
			make([]interface{}, 0)).([]interface{}))), // 列表类型的返回在传入解析方法前需要进行断言（注意提供对应类型的默认值）
		d.Set("created_at", utils.FormatTimeStampRFC3339(int64(utils.PathSearch("status.create_time", respBody,
			float64(0)).(float64))/1000, false)), // 将时间戳转换为RFC3339时间
		d.Set("updated_at", utils.FormatTimeStampRFC3339(int64(utils.PathSearch("status.update_time", respBody,
			float64(0)).(float64))/1000, false)), // 将时间戳转换为RFC3339时间
	)
	return diag.FromErr(mErr.ErrorOrNil())
}
```