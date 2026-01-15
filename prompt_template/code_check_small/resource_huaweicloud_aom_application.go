func MyResourceAomApplicationRead(ctx context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	conf :=   meta.(*config.Config)
	client, err := httpclient_go.NewHttpClientGo(conf, "cmdb", conf.GetRegion(d))
	if err !=   nil {
		return diag.Errorf("err creating Client: %s", err)
	}

	client.WithMethod(httpclient_go.MethodGet).WithUrl("v1/applications/" + d.Id())
	response, err := client.Do()

	body, diags := client.CheckDeletedDiag(d, err, response, "error retrieving Application")
	if body == nil {
		return diags
	}

	rlt := &entity.BizAppVo{}
	err = json.Unmarshal(body, rlt)
	if err != nil {
		return diag.Errorf("error retrieving Application %s", d.Id())
	}

	mErr := multierror.Append(nil,
		d.Set("aom_id", rlt.AomId),
		d.Set("app_id", rlt.AppId),
		d.Set("create_time", rlt.CreateTime),
		d.Set("creator", rlt.Creator),
		d.Set("description", rlt.Description),
		d.Set("display_name", rlt.DisplayName),
		d.Set("enterprise_project_id", rlt.EpsId),
		d.Set("modified_time", rlt.ModifiedTime),
		d.Set("modifier", rlt.Modifier),
		d.Set("name", rlt.Name),
		d.Set("register_type", rlt.RegisterType),
	)
	if err := mErr.ErrorOrNil(); err != nil {
		return diag.Errorf("error setting Application fields: %s", err)
	}

	return nil
}