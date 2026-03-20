	//Demo
	layui.use('form', function(){
	  var form = layui.form;
	  //监听提交
	  form.on('submit(formDemo)', function(data){
	  layer.alert('正在开发中.....', {icon: 5}); 
		var body={};
		//客户单号
		body.ref_no=data.field.ref_no;
		//渠道
		body.logistics_service_info={"logistics_product_code":data.field.logistics_product_code}
		//包裹列表
		body.parcel_list=[{"weight":data.field.weight}]
		//收件人信息
		body.recipient_info={"country":data.field.ri_country}
		//JSON序列化输出
		$("#code").text(JSON.stringify(body));
		console.log(data.field);
	    return false;
	  });
	  form.on('radio(include_battery)', function(data){
	    if(data.value=="Y"){
	    layer.msg('请输入电池类型如：996');
	    $("#battery_type").removeClass("layui-hide");
	    }else{
	    $("#battery_type").addClass("layui-hide");
	    }
	    // console.log(); //被点击的radio的value值
	  }); 
	  form.on('radio(sender)', function(data){
	    if(data.value=="Y"){
	    layer.msg('请输入发件人信息');
	    $("#sender").removeClass("layui-hide");
	    }else{
		layer.msg('使用默认发件人信息');
	    $("#sender").addClass("layui-hide");
	    }
	  });
	  
	});