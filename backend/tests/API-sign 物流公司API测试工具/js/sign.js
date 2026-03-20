//Demo
	layui.use('form', function(){
	var form = layui.form;
	//获取基础配置信息
	console.log("-----json-----");
	console.log(api_data);
	console.log("-----end------");
	//定义sign组成
	var signbody='';
	function config_init(data){
		//判断数据
		if(data.api_xms.length<1){
			layer.alert('请在config/api_data.js 文件下配置api接口信息', {icon: 5});
			return false;
		}else if(data.app.length<1){
			layer.alert('请在config/api_data.js 文件下配置app接口信息', {icon: 5});
			return false;
		}else{
			console.log("渲染app数据");
			//渲染app数据
			$(data.app).each(function(i){
				if(i==0){
				$("#AppKey").val(data.app[i].AppKey);
				$("#AppSecret").val(data.app[i].AppSecret);	
				}else{
					
				}
			});
			console.log("渲染api数据");
			//渲染api数据
			type_info1('xms');
			//渲染html
			form.render(); 
			
		}
	}
	config_init(api_data);

	function type_info1(type){
		var type_info='api_xms';
		if(type=='xms'){
			type_info='api_xms'
			$("#api_link").attr('href',api_data.api_xms[0].url);
			$("#api_link").text(api_data.api_xms[0].url);
		}
		else if(type=='fb4'){
			type_info='api_fb4'
			$("#api_link").attr('href',api_data.api_fb4[0].url);
			$("#api_link").text(api_data.api_fb4[0].url);
		}else if(type=='pub'){
			type_info='api_pub'
			$("#api_link").attr('href',api_data.api_pub[0].url);
			$("#api_link").text(api_data.api_pub[0].url);
		}
		$("#method option").remove();
		$("#v option").remove();
	//渲染api数据
	$(api_data[type_info]).each(function(i){
		if(i==0){
		$("#method").append('<option data="'+ api_data[type_info][i].url+'"  value="'+ api_data[type_info][i].method+'" v="'+api_data[type_info][i].v+'" selected>'+api_data[type_info][i].title+'</option>');	
		$("#v").append('<option value="'+ api_data[type_info][i].v +'" selected>'+api_data[type_info][i].v+'</option>');	
		}else{
		$("#method").append('<option data="'+ api_data[type_info][i].url+'" value="'+ api_data[type_info][i].method+'" v="'+api_data[type_info][i].v+'">'+api_data[type_info][i].title+'</option>');
		}
	});

}

		
		
	//判断是否一个json对象
	function isJsonString(str) {
	        try {
	            if (typeof JSON.parse(str) == "object") {
	                return true;
	            }
	        } catch(e) {
						layer.msg("json格式异常，请检查!"); 
	        }
	        return false;
		}
	
	  //监听提交
	  form.on('submit(formDemo)', function(data){
		  if(!isJsonString($("#aaa").val())){
			layer.msg("请求失败，json格式不正确"); 
			 return false;
		  }
		  layer.msg("请求成功,请求body已自动压缩,");  
		//APP
		var AppKey = $.trim(data.field.AppKey);
		var AppSecret = $.trim(data.field.AppSecret);
		//请求接口
		var method = data.field.method;
		//请求版本
		var v = data.field.v;
		//请求环境
		var url = data.field.url;
		//请求body
		var body =format1($.trim(data.field.body),true);
		//时间戳
		var timestamp = 0;
		if ($("#timestamp").hasClass("layui-hide")){
			//请求时间-系统当前时间戳
			 timestamp = (new Date()).getTime();
		}else{
			timestamp = data.field.timestamp;
		}

		//sign组合
		var sign = "app_key"+AppKey+"formatjson"+"method"+method+"timestamp"+timestamp+"v"+v+body+AppSecret;
		signbody = sign;
		//MD5加密32位小$.md5
		var md5 = $.md5(sign)
		$("#md5").html(md5);
		//请求url 注意&times显示在html会变成X 我这里用这个&amp代替&
		$("#url").html(url+"?method="+method+"&app_key="+AppKey+"&v="+v+"&amp"+"timestamp="+timestamp+"&format=json&"+"sign="+md5);
		//请求body
		$("#aaa").val(body);
		$("#body").text(body);
		// $("#code").text(JSON.stringify(sign));
		console.log(data.field);
		form.render();
	    return false;
	  });
	  //使用format(json,true）;表示压缩json字符串。format(json,false）;表示格式化json字符串。
	  function format1(txt, compress) { /*格式化jsON源码(对象转换为jsON文本,是否为压缩模式)*/
	  	 	var indentChar = ' ';
	  	 	if (/^\s*$/.test(txt)) {
	  	 		layer.msg('数据为空,无法格式化! ');
	  	 		return 0;
	  	 	}
	  	 	try {
	  	 		var data = eval('(' + txt + ')');
	  	 	} catch (e) {
	  	 		layer.msg('数据源语法错误,格式化失败! 错误信息: ' + e.description, 'err');
	  	 		return 0;
	  	 	};
	  	 	var draw = [],
	  	 		last = false,
	  	 		This = this,
	  	 		line = compress ? '' : '\n',
	  	 		nodeCount = 0,
	  	 		maxDepth = 0;
	  	 
	  	 	var notify = function(name, value, isLast, indent /*缩进*/ , formObj) {
	  	 		nodeCount++; /*节点计数*/
	  	 		for (var i = 0, tab = ''; i < indent; i++) tab += indentChar; /* 缩进html */
	  	 		tab = compress ? '' : tab; /*压缩模式忽略缩进*/
	  	 		maxDepth = ++indent; /*缩进递增并记录*/
	  	 		if (value && value.constructor == Array) { /*处理数组*/
	  	 			draw.push(tab + (formObj ? ('"' + name + '":') : '') + '[' + line); /*缩进'[' 然后换行*/
	  	 			for (var i = 0; i < value.length; i++)
	  	 				notify(i, value[i], i == value.length - 1, indent, false);
	  	 			draw.push(tab + ']' + (isLast ? line : (',' + line))); /*缩进']'换行,若非尾元素则添加逗号*/
	  	 		} else if (value && typeof value == 'object') { /*处理对象*/
	  	 			draw.push(tab + (formObj ? ('"' + name + '":') : '') + '{' + line); /*缩进'{' 然后换行*/
	  	 			var len = 0,
	  	 				i = 0;
	  	 			for (var key in value) len++;
	  	 			for (var key in value) notify(key, value[key], ++i == len, indent, true);
	  	 			draw.push(tab + '}' + (isLast ? line : (',' + line))); /*缩进'}'换行,若非尾元素则添加逗号*/
	  	 		} else {
	  	 			if (typeof value == 'string') value = '"' + value + '"';
	  	 			draw.push(tab + (formObj ? ('"' + name + '":') : '') + value + (isLast ? '' : ',') + line);
	  	 		};
	  	 	};
	  	 	var isLast = true,
	  	 		indent = 0;
	  	 	notify('', data, isLast, indent, false);
	  	 	return draw.join('');
	  	 }

		 //json 压缩
		 $("#y_json").click(function(){
		 		var data1 = $("#aaa").val();
				if(isJsonString(data1)){
					$("#aaa").val(format1(data1,true));
					$("#body").text($("#aaa").val());
					layer.msg("压缩成功");
				}

		 });
		 //json 格式化
		 $("#j_json").click(function(){
		 	var data1 = $("#aaa").val();
		 	if(isJsonString(data1)){
		 		$("#aaa").val(format1(data1,false));
				$("#body").text($("#aaa").val());
		 		layer.msg("格式化成功");
		 	}
		 });
	  //判断选择的接口-更新渲染版本号
	  form.on('select(method)', function(data){
		  console.log("是否执行了接口");
	    var v =$("[value='"+data.value+"']").attr("v"); //获取版本值
		//删除元素
		$("#v").empty();
		$("#v").append('<option value="'+ v +'" selected>'+v+'</option>');	
		var url=$("#method").find("option:selected").attr('data');
		$("#api_link").attr('href',url);
		$("#api_link").text(url);
		//更新渲染
		form.render();
	  });  
	//判断选择环境
	form.on('radio(type)', function(data){
				if(data.value=='全球直发'){
					layer.msg("全球直发-XMS");
					//渲染api数据
					$("#http_test").removeAttr("disabled");
					type_info1('xms');
				}else if(data.value=='订单履约'){
					layer.msg("订单履约-FB4,测试环境无法使用");
					$("#http_test").attr("disabled","disabled");
					$("#http_test").removeAttr("checked");
					$("input[name=url][value='https://open.4px.com/router/api/service']").prop("checked","true");
					// $("#http_sc").attr('checked','checked');
					console.log("是否執行了FB4");
					type_info1('fb4');
				}else if(data.value=='公共服务'){
					layer.msg("公共服务,测试环境无法使用");
					$("#http_test").attr("disabled","disabled");
					$("#http_test").removeAttr("checked");
					$("input[name=url][value='https://open.4px.com/router/api/service']").prop("checked","true");
					// $("#http_sc").attr('checked','checked');
					console.log("是否執行了pub");
					type_info1('pub');
				}
			form.render();
	});   
	  
	  
	  //判断选择环境
	  form.on('radio(url)', function(data){
			if(data.value=='https://open.4px.com/router/api/service'){
				layer.msg("选择了生成环境");
				//判断是否配置默认，如果没有配置默认，需要客户输入生产环境的app
				console.log(api_data.app[1].AppKey);
				if($.trim(api_data.app[1].AppKey)==""||$.trim(api_data.app[1].AppSecret)==""){
					//请输入生产环境的AppKey和AppSecret
					layer.msg("请输入生产环境的AppKey和AppSecret");
					$("#AppKey").val("");
					$("#AppSecret").val("");
				}else{
					//填入配置信息的AppKey和AppSecret
					$("#AppKey").val(api_data.app[1].AppKey);
					$("#AppSecret").val(api_data.app[1].AppSecret);
				}
			}else if(data.value=='https://open-test.4px.com/router/api/service'){
				layer.msg("选择了测试环境");
				$("#AppKey").val(api_data.app[0].AppKey);
				$("#AppSecret").val(api_data.app[0].AppSecret);
			}
	  		form.render();
	  }); 
	  
	 //判断是否自定义时间戳
	  form.on('checkbox(usertime)', function(data){
		  if(data.elem.checked==true){
			layer.msg('请输入自定义时间戳');
		  $("#timestamp").removeClass("layui-hide");
		  }else{
			layer.msg('开启系统请求时间');
		  $("#timestamp").addClass("layui-hide");
		  }
	  });
	  
	  //复制url
	  $("#copy_u").click(function(){
	     if($.trim($("#url").text())==""){
	  	 layer.alert('兄弟没有内容,请先生成内容', {icon: 5});
	     }else{
	  	layer.alert('复制成功', {icon: 1}); 
		Clipboard.copy($("#url").text());
	     }
	  });
	  //复制MD5
	  $("#copy_m").click(function(){
	     if($.trim($("#md5").text())==""){
	     			 layer.alert('兄弟没有内容,请先生成内容', {icon: 5});
	     }else{
	     			layer.alert('复制成功', {icon: 1}); 
					Clipboard.copy($("#md5").text());
	     }
	  });
	  //复制url
	  $("#copy_b").click(function(){
	    if($.trim($("#body").text())==""){
	     			 layer.alert('兄弟没有内容,请先生成内容', {icon: 5});
	     }else{
	     			layer.alert('复制成功', {icon: 1}); 
					 Clipboard.copy($("#body").text());
	     }
	  });
	//点击查看sign组成
	  $("#copy_sign").click(function(){
		if(signbody==""){
		layer.alert('兄弟没有内容,请先生成内容', {icon: 5});
		}else{
		layer.open({
		  title: 'sign组成'
		  ,content: signbody+'<button id="signbody" type="button" 	class="layui-btn layui-btn-xs" style="margin-left: 10px;">复制</button>'
		});  	
		}  
		 //监听signbody复制
		 //复制url
		 $("#signbody").click(function(){
		   if($.trim($("#signbody").text())==""){
		    			 layer.alert('兄弟没有内容,请先生成内容', {icon: 5});
		    }else{
		    			layer.alert('复制成功', {icon: 1}); 
		 					 Clipboard.copy(signbody);
		    }
		 });
	  });
	});

