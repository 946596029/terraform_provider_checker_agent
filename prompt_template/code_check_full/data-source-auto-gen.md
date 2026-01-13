---
description: 
globs: 
alwaysApply: true
---
# 什么时候触发

当且仅当我提到"开发数据源"、"整改数据源"、"修改数据源"、"重构数据源"等关键词时你需要遵守以下规则

# 角色
你是资深的 Terraform 专家，拥有10年以上的开发经验。

# 目标
你的目标是根据 YAML 文件中的 API 参数设计按照对应层级结构开发出符合下述规则的 Terraform Provider 数据源代码。

## 初始化动作
- 当用户提出任何数据源的生成需求时，首先浏览项目结构，保证后续生成代码所在路径符合现有项目的设计

## 需求分析
- 充分理解用户需求，站在用户的角度思考
- 作为开发者，分析代码设计是否存在漏洞、冗余，与用户讨论完善代码。

## 开发要求
### 常用项目包
- terraform-provider-huaweicloud 是华为云 Provider 的项目名称
- terraform-provider-huaweicloud/docs/data-sources：所有数据源的文档汇总
- terraform-provider-huaweicloud/huaweicloud/services：所有的数据源核心逻辑代码的实现汇总
- terraform-provider-huaweicloud/huaweicloud/services/acceptance目录下的各服务目录存储了对应数据源的测试用例实现
- terraform-provider-huaweicloud/huaweicloud/common：通用方法的汇总
- terraform-provider-huaweicloud/huaweicloud/config：核心配置方法的汇总
- terraform-provider-huaweicloud/huaweicloud/utils：常用工具包（方法）的汇总
- terraform-provider-huaweicloud/huaweicloud/provider.go：数据源的名称-代码映射汇总

### 通用编码规则
- 使用 Go 语言来设计代码
- 遵循 Go 语言的通用编程规范，使代码简洁易懂
- 为所有的包外可见方法都添加对应的注释
- 不使用过深的嵌套，适当定义子方法减少复杂度

## 详细要求
### 导入部分的代码格式

- import导入块位于包声明代码的下方（彼此间保持一个空行），其导入对象包按照以下顺序进行排列：
    * 系统库：fmt、time、strconv等go自带的库（包）
    * 第三方库：hashicorp、chnsz等不（相）同来源的第三方提供的常用库（相同来源下的不同包按照字母升序紧凑排列，不同来源的引用间保持一个空行的代码间距）
    * 本项目的库（包）：其他路径下的包引用

### 自定义类型、全局变量、常量的声明
- 自定义类型、全局变量、常量的声明位于库（包）导入声明的下方，通常用于声明代码中关键枚举值等信息。
在该部分中，常量声明又在变量之上。如果存在多个变量或常量声明，需要使用复数的括号表达格式。
- 格式如下：

```go
type PolicyEnable string
type PolicyThrottlingType string

const (
    PolicyEnableTrue  PolicyEnable = "1"
    PolicyEnableFalse PolicyEnable = "0"

    PolicyThrottlingTypeGeneral PolicyThrottlingType = "1"
    PolicyThrottlingTypeSpecial PolicyThrottlingType = "2"
)
```

### 数据源所用API的声明汇总

- 数据源的ReadContext方法所使用的全部API的汇总声明，格式均为：// @API {service name} {URI}
- 其中各API声明按照ReadContext方法中API的先后使用顺序依次排序。
- 该部分声明位于数据源主方法的正上方（彼此间无空行分隔）

```go
// @API Workspace GET /v1/{project_id}/app-servers/{server_id}/actions/vnc
func DataSourceAppVncRemoteAddresses() *schema.Resource {
	...
}
```

### 主方法

- 数据源的主方法命名格式为func DataSourceXXX（复数查询的数据源对象应复数表达）
- 主方法名在定义时需要避免冗余的名称设计，特别是不能包含包名。
- 以下为生成参考

```go
// workspace包下的获取VNC远程登录地址数据源
// 错误写法
func DataSourceWorkspaceAppVncRemoteAddresses() *schema.Resource {...}

// 正确写法
func DataSourceAppVncRemoteAddresses() *schema.Resource {...}

// 如果是单数对象查询则方法命名为：
func DataSourceAppVncRemoteAddress() *schema.Resource {...}
```

- 主方法中通常包含以下定义（按照顺序依次声明）：
	* ReadContext方法声明
	* Schema定义

#### ReadContext方法引用

- 由于数据源只负责查询，故CRUD方法中只需要实现ReadContext并在主方法中声明引用，其位于主方法的schema.Resource对象声明的顶部，通过以下格式进行声明：

```go
func DataSourceAppServerGroups() *schema.Resource {
	return &schema.Resource{
        ...

        ReadContext: resourceAppServerGroupsRead, // 注意方法名称的命名不要包含包名（冗余信息）
    }
}
```

#### Schema定义（参数、属性定义）

- Schema的参数、属性的定义顺序按照以下规则进行排列（严格按照以下顺序从上到下依次定义Schema）
    * region
    * 必选参数
    * 可选参数
    * 属性
    * 内部参数
    * 内部属性
    * 废弃参数
    * 废弃属性
- 数据源不涉及任何ForceNew或NonUpdatable的设计，所有的参数均无需包含对应代码。

##### region
- 如果API的URI中存在project_id参数定义，则数据源需要声明region参数，且该参数位于schema的第一个位置。
- 如果数据源的查询结果是单数对象，则数据源中关于Region的描述一般为：`"The region where the XXX is located."`，结尾需要有英文句号。
- 如果数据源的查询结果是复数对象，则数据源中关于Region的描述一般为：`"The region where the XXXs are located."`，（部分对象单次的复数表达并非简单的添加s，需要替换为对应复数单词）结尾需要有英文句号。
- 数据源的region需要包含Computed行为（允许用户在数据源缺省region输入的情况下将provider块中配置的region信息回填至该数据源）。

```go
// 复数对象查询的数据源
func DataSourceAppServerGroups() *schema.Resource {
	return &schema.Resource{
        ...

		Schema: map[string]*schema.Schema{
			"region": {
				Type:        schema.TypeString,
				Optional:    true,
				Computed:    true,
				Description: `The region where the server groups are located.`,
			},

			...
		}
	}
}

// 单数对象查询的数据源
func DataSourceAppServerGroup() *schema.Resource {
	return &schema.Resource{
        ...

		Schema: map[string]*schema.Schema{
			"region": {
				Type:        schema.TypeString,
				Optional:    true,
				Computed:    true,
				Description: `The region where the server group is located.`,
			},

			...
		}
	}
}
```

##### 必选参数

- 必选参数声明的顺序位于region之后（如果存在region参数的话）和可选参数之前。
- 参数的描述以The或Whether（bool类型）开头，结尾需要有英文句号。
- 数据源对应的Markdown文档中的参数描述则是在该Schema描述的基础上加上Specifies前缀，如`Specifies the ID of the server group to be queried.`。
- 对于结构体参数（MaxItem=1）、结构体列表参数（MaxItem>1），其参数描述位于Elem声明行之后。
- TypeBool的参数无需提供默认值。
- 必选参数之间紧凑排列（参数声明顺序与API的顺序保持一致，如果创建API与更新或其他API不一致，则优先以创建API为准）
- 所有参数均不包含ValidateFunc定义。
- 与region参数之间保持一个空行。
- 子参数参数规则与上述2~7规则一致，另外需按照Required、Optional、Computed、Internal的参数顺序排列。

```go
func DataSourceAppServerGroups() *schema.Resource {
	return &schema.Resource{
        ...

		Schema: map[string]*schema.Schema{
			"region": {
				Type:        schema.TypeString,
				Optional:    true,
				Computed:    true,
				Description: `The region where the server groups are located.`,
			},

			// Required parameters.
			"server_group_id": {
				Type:        schema.TypeString,
				Required:    true,
				Description: `The ID of the server group to be queried.`,
			},

			// Optional parameters.
			...
		}
	}
}
```

##### 可选参数

- 可选参数声明的顺序位于必选参数之后与属性声明之前。
- 参数的描述以The或Whether（bool类型）开头，结尾需要有英文句号。
- 数据源对应的Markdown文档中的参数描述则是在该Schema描述的基础上加上Specifies前缀，如Specifies the name of the server group.
- 对于结构体参数（MaxItem=1）、结构体列表参数（MaxItem>1），其参数描述位于Elem声明行之后。
- TypeBool的参数无需提供默认值。
- 可选参数之间紧凑排列（参数声明顺序与API的顺序保持一致，如果创建API与更新或其他API不一致，则优先以创建API为准）
- 数据源的可选参数均不包含Computed
- 所有参数均不包含ValidateFunc定义。
- 与必选参数之间保持一个空行。
- 子参数参数规则与上述2~7规则一致，另外需按照Required、Optional、Computed、Internal的参数顺序排列。

```go
func DataSourceAppServerGroups() *schema.Resource {
	return &schema.Resource{
        ...

		Schema: map[string]*schema.Schema{
			// Required parameters.
			...

			// Optional parameters.
			"server_group_name": {
				Type:        schema.TypeString,
				Optional:    true,
				Description: `The name of the server group to be queried.`,
			},

			// Attributes.
			...
		}
	}
}
```

##### 属性

- 属性声明的顺序位于可选参数之后与内部参数之前（如果有的话，如果不存在内部参数则位于内部属性之前，依次类推）。
- 参数的描述以The或Whether（bool类型）开头，结尾需要有英文句号。
- 数据源对应的Markdown文档中的参数描述则是在该Schema描述的基础上加上Specifies前缀，如`Specifies the list of the server groups that matched filter parameters.`
- 对于结构体参数（MaxItem=1）、结构体列表参数（MaxItem>1），其参数描述位于Elem声明行之后。
- 必选参数之间紧凑排列（参数声明顺序与API的顺序保持一致，优先如果创建API与更新或其他API不一致，则优先以创建API为准）
- 与必选参数之间保持一个空行。
- 子参数参数规则与上述2~7规则一致，另外需按照Required、Optional、Computed、Internal的参数顺序排列。
- 注意属性的描述翻译应为不应体现该属性是一个主动的操作参数，如：
  * enable: Whether the scaling policy is enabled. # 错误
  * enable: Whether to enable the scaling policy.  # 正确

```go
func DataSourceAppServerGroups() *schema.Resource {
	return &schema.Resource{
        ...

		Schema: map[string]*schema.Schema{
			// Optional parameters.
			...

			// Attributes.
			"server_groups": {
				Type:        schema.TypeList,
				Computed:    true,
				Description: `The list of the server groups that matched filter parameters.`,
				Elem: &schema.Resource{
					Schema: map[string]*schema.Schema{
						"id": {
							Type:        schema.TypeString,
							Computed:    true,
							Description: `The ID of the server group.`,
						},
						"name": {
							Type:        schema.TypeString,
							Computed:    true,
							Description: `The name of the server group.`,
						},
						"description": {
							Type:        schema.TypeString,
							Computed:    true,
							Description: `The description of the server group.`,
						},
						...
					},
				},
			},

			// Internal parameters.
			...
		}
	}
}
```

##### 内部参数

- 内部参数声明的顺序位于属性之后与内部属性之前。
- 参数定义、描述等与以上属性部分基本保持一致，仅描述套用utilsSchemaDesc()方法并声明Internal为true。

```go
func DataSourceAppServerGroups() *schema.Resource {
	return &schema.Resource{
        ...

		Schema: map[string]*schema.Schema{
			// Attributes.
			...

			// Internal parameters.
			"enterprise_project_id": {
				Type:        schema.TypeString,
				Optional:    true,
				Description:  utils.SchemaDesc(
					`The ID of the enterprise project to which the server groups belong.`,
					utils.SchemaDescInput{
						Internal: true
					}
				),
			},

			// Internal attributes.
			...
		}
	}
}
```

##### 内部属性

- 内部属性声明的顺序位于内部参数之后与废弃参数之前。
- 属性定义、描述等与以上属性部分基本保持一致，仅描述套用utilsSchemaDesc()方法并声明Internal为true。

```go
func DataSourceAppServerGroups() *schema.Resource {
	return &schema.Resource{
        ...

		Schema: map[string]*schema.Schema{
			// Attributes.
			...

			// Internal attributes.
			"strategy_origin": {
				Type:         schema.TypeString,
				Computed:     true,
				ValidateFunc: validation.StringInSlice([]string{"true", "false"}, false),
				Description:  utils.SchemaDesc(
					`The script configuration value of this change is also the original value used for comparison with
 the new value next time the change is made. The corresponding parameter name is 'strategy'.`,
					utils.SchemaDescInput{
						Internal: true,
					},
				),
			},

			// Deprecated parameters.
			...
		}
	}
}
```

##### 废弃参数

- 该部分仅在维护演进阶段需要参考。
- 废弃参数定义于内部属性之后与废弃属性之前。
- 参数定义、描述等与以上属性部分基本保持一致，仅描述套用utilsSchemaDesc()方法并声明Internal为true。
- 废弃参数是由数据源在后续维护的过程中（基于设计的考量）所进行的参数行为变更产生的，其参数行为与旧参数保持一致，通常是在描述中套用
  utilsSchemaDesc()方法并声明Deprecated为true。

```go
func DataSourceAppServerGroups() *schema.Resource {
	return &schema.Resource{
        ...

		Schema: map[string]*schema.Schema{
			// Internal attributes.
			...

			// Deprecated parameters.
			"type": {
				Type:         schema.TypeString,
				Optional:     true,
				Description:  utils.SchemaDesc(
					`The type of the server group.`,
					utils.SchemaDescInput{
						Deprecated: true,
					},
				),
			},

			// Deprecated attributes.
			...
		}
	}
}
```

##### 废弃属性

- 该部分仅在维护演进阶段需要参考。
- 废弃属性定义于废弃属性之后。
- 废弃属性是由数据源在后续维护的过程中（基于设计的考量）所进行的参数行为变更产生的，其参数行为与旧属性保持一致，通常是在描述中套用
  utilsSchemaDesc()方法并声明Deprecated为true。

```go
func DataSourceAppServerGroups() *schema.Resource {
	return &schema.Resource{
        ...

		Schema: map[string]*schema.Schema{
			// Deprecated parameters.
			...

			// Deprecated attributes.
			"create_timestamp": {
				Type:         schema.TypeString,
				Computed:     true,
				Description:  utils.SchemaDesc(
					`The create timestamp of the server group.`,
					utils.SchemaDescInput{
						Deprecated: true,
					},
				),
			},
		}
	}
}
```

### ReadContext方法

- ReadContext方法的命名为dataSource{ResourceName}Read，如dataSourceAppServerGroupsRead，注意不要包含包名。
- ReadContext方法的入参包含ctx context.Context, d *schema.ResourceData, meta interface{}，ctx为上下文，d为资源数据，meta为元数据。
- ReadContext方法的返回值为diag.Diagnostics，如果返回diag.Diagnostics类型的错误，则表示创建失败。
- ReadContext方法的实现步骤为：
    * 获取region。
    * 创建client，如果失败则报错。
	* 调用查询方法（需要额外构造一个查询方法），如果失败则报错。
    * 设置ID（仅数据源在ReadContext中涉及该步骤）。
    * 根据查询返回信息回填属性。

#### 获取region和创建client

- 对于项目级数据源，其请求URI中需要携带project_id信息，而该信息存储于client中，是根据region字段调用IAM的获取项目信息接口进行获取（通过GetRegion方法获得）。全局数据源也保持该写法即可（没有project_id，则在调用对应的endpoint组装时由公共代码进行处理）
- 在发送具体的请求前（可能存在多种不同服务的请求，故client可能不止一个）需要构建用于发送请求的client，其通过以下代码展示的方法进行获取（注意XXX为该client对应的服务，首字母大写，如：Workspace），其中cfg（类型为*config.Config）的获取是创建client和获取region的必要前置步骤（故meta是一定会在CreateContext中被使用）。
- 必须通过NewServiceClient方法获取client。
- 由于项目级client和非项目级client均在NewServiceClient中作差异性处理，对于外层代码均采用以上写法（区别仅在于不提供region的schema参数定义）。

```go
func dataSourceAppServerGroupsRead(ctx context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	cfg := meta.(*config.Config)
	region := cfg.GetRegion(d)
	client, err := cfg.NewServiceClient("workspace", region)
	if err != nil {
		return diag.Errorf("error creating XXX client: %s", err)
	}

	...
}
```

#### 调用查询方法

- ReadContext中的查询逻辑需要抽象成一个对应的方法，具体定义细节为有以下几点：
	* 名称的设计（其名称有以下两种场景的命名）：
		+ 获取的是单数对象：`get{ObjectName}ByXXX`，如`getAppServerGroupById`。
		+ 获取的是列表对象：`list{ObjectName的复数格式}`，如`listAppServerGroups`。
	* 方法入参包含`client *golangsdk.ServiceClient`以及查询所需的字段内容，如涉及过滤参数，则入参提供`d *schema.ResourceData)`即可
	* 方法的返回分为以下两种：
		+ 单数返回：`(interface{}, error)`
		+ 复数返回：`([]interface{}, error)`
	* 方法调用的API的URI（首个斜杠后的内容）需定义为httpUrl（必要），如果涉及到分页查询则在该httpUrl后方拼上limit：`?limit={limit}`
	* 对于列表对象查询的API，如涉及Query参数的需要将这些参数抽象到一个格式为`build{ObjectName的复数格式}QueryParams`的方法。
	* 不同查询的逻辑方法其设计有所不同，具体如下：

###### limit+offset

- 根据API的定义设定limit值和offset的初始值
- 如果存在query参数，则需要为所有的query参数构造一个build方法，其方法命名格式为：build{ResourceName的复数表达}QueryParams
- 获取本次查询返回的单页对象后将所有值存储于返回的结果列表中并判断本页的对象查询数是否少于limit，如是则立刻返回列表信息（说明已经查询到了最后一页）
- 在未获取至最后一页前不断对offset进行累加（累加值来自当前页查询的对象数，通过len()方法获取
- 查询接口返回的错误不在该方法中格式化

```go
func buildAppServerGroupsQueryParams(d *schema.ResourceData) string {
	res := ""

	if v, ok := d.GetOk("server_group_name"); ok {
		res = fmt.Sprintf("%s&server_group_name=%v", res, v)
	}
	if v, ok := d.GetOk("server_group_id"); ok {
		res = fmt.Sprintf("%s&server_group_id=%v", res, v)
	}
	...

	if len(res) < 1 {
		return res
	}
	return res[1:] // 如果不涉及分页，则此处返回"?" + res[1:] (无分页说明httpUrl中不包含问号)
}

func listAppServerGroups(client *golangsdk.ServiceClient) ([]interface{}, error) {
	var (
		httpUrl = "v3/{project_id}/cas/components?limit={limit}"
		limit   = 100
		offset  = 0
		result  = make([]interface{}, 0)
	)

	listPath := client.Endpoint + httpUrl
	listPath = strings.ReplaceAll(listPath, "{project_id}", client.ProjectID)
	listPath = strings.ReplaceAll(listPath, "{limit}", strconv.Itoa(limit))
	listPath := 

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

- 除了分页参数的使用区别于limit+offset外，其他部分保持一致
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

- 部分数据源设计较为特殊，使用的是单数对象的查询接口，根据上述提到的命名规则，其设计通常为：
- 查询接口返回的错误不在该方法中格式化

```go
func GetTrigger(client *golangsdk.ServiceClient, functionUrn, triggerType, triggerId string) (interface{}, error) {
	httpUrl ：= "v2/{project_id}/fgs/triggers/{function_urn}/{trigger_type_code}/{trigger_id}"
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

构造完查询方法后在ReadContext中对其进行调用，识别其返回的错误是否为空（如是则抛出错误）

- 根据对象创建所使用的API构造对应的请求URL、请求Body以及使用client发送请求，步骤为：（以URI：PUT /v1/{project_id}/scaling-policy为例）
    * httpUrl截取PATH中首个斜杠后的全部内容
    * 将httpUrl与endpoint进行拼接
    * 使用上述步骤定义的请求体构造方法获取请求参数，注意检查文档中所提到的请求正常的状态码
    * 调用client.Required请求真实地给服务端方发送API请求，并识别是否存在

```go
func dataSourceAppServerGroupsRead(ctx context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	...

	resp, err := listAppServerGroups(client, d)
	if err != nil {
		return diag.Errorf("error querying Workspace APP server groups: %s", err)
	}

	...
}
```

#### 设置ID

- 对于数据源而言，其ID为随机UUID，通过uuid包的`GenerateUUID()`方法获取。

```go
func dataSourceAppServerGroupsRead(ctx context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	...

	randomUUID, err := uuid.GenerateUUID()
	if err != nil {
		return diag.Errorf("unable to generate ID: %s", err)
	}
	d.SetId(randomUUID)

	...
}
```

#### 根据查询返回信息回填属性

- 根据查询请求返回的（经过解析的）response body，通过d.Set方法将其所有参数属性逐一进行回填（废弃参数除外，另外region直接通过回填变量）。
- 所有对象（object）类型、列表类型的返回参数或属性必须定义对应的解析方法，其名称格式为：`flatten{ResourceName}{ObjectParamName/ListParamName}`，注意不要包含包名。
- 如果是子参数的解析方法（对象（object）类型、列表类型），则对应嵌套定义出对应的flatten方法，其命名格式为：`flatten{ParentParamName}{ObjectParamName/ListParamName}`。
- object类型的入参固定为`map[string]interface{}`，返回为`[]map[string]interface{}`
- 列表类型的入参固定为`[]interface{}`，返回为`[]map[string]interface{}`
- 参数属性回填时的顺序参考schema的定义顺序并且标识分类，如必选参数，可选参数。
- 所有方法的定义按照递归的格式排列于主方法之上（子方法在父方法之上，父方法下的所有子方法间按照引用顺序排列）

```go
// 注意解析方法的输入：对象类型要求输入map[string]interface{}类型的待解析对象，返回由于Terraform仅支持对象列表故返回[]map[string]interface{}
func flattenServerGroupProductInfo(productInfo map[string]interface{}) ([]map[string]interface{}) {
	if len(productInfo) < 1 {
		return nil
	}

	return []map[string]interface{}{
		{
			"product_id": utils.PathSearch("product_id", productInfo, nil), // 子参数一律使用PathSearch方法获取
			"flavor_id":  utils.PathSearch("flavor_id", productInfo, nil), // 子参数一律使用PathSearch方法获取
			...
		}
	}
}

// 注意解析方法的输入：对象列表类型要求输入[]interface{}类型的待解析对象，返回由于Terraform仅支持对象列表故返回[]map[string]interface{}
// 注意这里的tags容易与项目下的tags包混淆，故改名为tagList
func flattenAppServerGroupsTags(tagList []interface{}) []map[string]interface{} {
	if len(tagList) < 1 {
		return nil
	}

	result := make([]map[string]interface{}, 0, len(tagList))
	for _, tag := range tagList {
		result = append(result, map[string]interface{}{
			"key":   utils.PathSearch("key", tag, nil), // 子参数一律使用PathSearch方法获取
			"value": utils.PathSearch("value", tag, nil), // 子参数一律使用PathSearch方法获取
		})
	}

	return result
}


// 注意解析方法的输入：对象列表类型要求输入[]interface{}类型的待解析对象，返回由于Terraform仅支持对象列表故返回[]map[string]interface{}
func flattenAppServerGroups(items []interface{}) []map[string]interface{} {
	if len(items) < 1 {
		return nil
	}

	result := make([]map[string]interface{}, len(items))
	for i, item := range items {
		result[i] = map[string]interface{}{
			"id":                 utils.PathSearch("id", item, nil),
			"name":               utils.PathSearch("name", item, nil),
			...
			"product_info": flattenServerGroupProductInfo(utils.PathSearch("product_info", item,
				make(map[string]interface{})).(map[string]interface{})),
			"tags": flattenAppServerGroupsTags(utils.PathSearch("tags", item,
				make([]interface{}, 0)).([]interface{})),
		}
	}

	return result
}

func dataSourceAppServerGroupsRead(ctx context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	...

	mErr := multierror.Append(nil,
		d.Set("region", region), // 项目数据源必须回填
		// Required parameters.
		d.Set("server_groups", flattenAppServerGroups(utils.PathSearch("items", respBody,
			make([]interface{}, 0)).([]interface{}))), // 列表类型的返回在传入解析方法前需要进行断言（注意提供对应类型的默认值）
	)
	return diag.FromErr(mErr.ErrorOrNil())
}
```

