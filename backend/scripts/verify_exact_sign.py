"""
使用HTML工具生成的精确参数验证签名算法
"""
import hashlib
import json

# 生产环境账号
APP_KEY = "6efa9a05-5e31-4d2a-9a9c-da7624627f26"
APP_SECRET = "0b768497-0c7a-4247-a7c0-0ca20cb2ae16"

# HTML工具生成的数据
HTML_TIMESTAMP = "1773045160876"
HTML_SIGN = "4bc0d9d294f68c3bfc64aca248cda7c9"

# 从sign组成中提取的JSON（HTML工具实际使用的）
HTML_JSON = '{"4px_tracking_no":"","ref_no":"YIN201803280000002","business_type":"BDS","duty_type":"U","cargo_type":"5","vat_no":"8956232323","eori_no":"8956232323","buyer_id":"aliwangwang","sales_platform":"ebay","seller_id":"cainiao","logistics_service_info":{"logistics_product_code":"F3","customs_service":"N","signature_service":"N","value_added_services":""},"label_barcode":"","return_info":{"is_return_on_domestic":"Y","domestic_return_addr":{"first_name":"ZHANG_return","last_name":"YU_return","company":"fpx_return","phone":"8956232659","phone2":"18562356856","email":"return_ZHANGYZ@4PX.COM","post_code":"518000","country":"CN","state":"广东省__return","city":"深圳市_return","district":"宝安区_return","street":"财富港大厦D座25楼__return","house_number":"16"},"is_return_on_oversea":"Y","oversea_return_addr":{"first_name":"ZHANG_return_oversea","last_name":"YU_return_oversea","company":"fpx_return_oversea","phone":"8956232659","phone2":"18562356856","email":"ZHANGYZ@4PX_return_oversea.COM","post_code":"518000","country":"CN","state":"state_return_oversea","city":"city_return_oversea","district":"district__return_oversea","street":"street_return_oversea","house_number":"17"}},"parcel_list":[{"weight":22,"length":123,"width":789,"height":456,"parcel_value":666.66,"currency":"USD","include_battery":"Y","battery_type":"966","product_list":[{"sku_code":"iPhone6  plus_sku_code","standard_product_barcode":"56323598","product_name":"iPhone6  plus_product_name","product_description":"iPhone6  plusiPhone6  plus_product_description","product_unit_price":3,"currency":"USD","qty":3}],"declare_product_info":[{"declare_product_code":"62323_declare_product_code","declare_product_name_cn":"手机贴膜_declare_name_cn","declare_product_name_en":"phone_declare_product_name_en","uses":"装饰_uses","specification":"dgd23_specification","component":"塑料_component","unit_net_weight":20,"unit_gross_weight":45,"material":"565323","declare_product_code_qty":2,"unit_declare_product":"个","origin_country":"中国","country_export":"越南","country_import":"新加坡","hscode_export":"45673576397","hscode_import":"12332213134","declare_unit_price_export":23,"currency_export":"USD","declare_unit_price_import":1.25,"currency_import":"USD","brand_export":"象印","brand_import":"虎牌","sales_url":"http://172.16.30.134:8038/loggerMessage/","package_remarks":"skutest"}]}],"is_insure":"Y","insurance_info":{"insure_type":"8Y","insure_value":2,"currency":"USD","insure_person":"张三_insure_person","certificate_type":"ID","certificate_no":"429001198806253256","category_code":"","insure_product_name":"手机壳insure_product_name","package_qty":"2"},"sender":{"first_name":"ZHANG_sender","last_name":"YU_sender","company":"fpx_sender","phone":"8956232659","phone2":"18562356856","email":"ZHANGYZ_sender@4PX.COM","post_code":"518000","country":"CN","state":"state_sender","city":"city_sender","district":"district_sender","street":"street_sender","house_number":"18","certificate_info":{"certificate_type":"PP","certificate_no":"965232323232656532","id_front_url":"https://ju.taobao.com/jusp/other/mingpin/tp.htmbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","id_back_url":"https://ju.taobao.com/jusp/other/mingpin/tp.htmcccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"}},"recipient_info":{"first_name":"ZHANG_recipient","last_name":"YU_recipient","company":"fpx_recipient","phone":"8956232659","phone2":"18562356856","email":"ZHANGYZ_recipient@4PX.COM","post_code":"518000","country":"SG","state":"state_recipient","city":"city_recipient","district":"district_recipient","street":"street_recipient","house_number":"19","certificate_info":{"certificate_type":"ID","certificate_no":"965232323232656532","id_front_url":"https://ju.taobao.com/jusp/other/mingpin/tp.htm?spm=875.7931836/ddddddddddddddddddddddddddddddddddddddddddddd","id_back_url":"https://ju.taobao.com/jusp/other/mingpin/tp.htmeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"}},"deliver_type_info":{"deliver_type":"2","warehouse_code":"","pick_up_info":{"expect_pick_up_earliest_time":"1432710115000","expect_pick_up_latest_time":"1432710115000","pick_up_address_info":{"first_name":"ZHANG_pick_up","last_name":"YU_pick_up","company":"fpx_pick_up","phone":"8956232659","phone2":"18562356856","email":"ZHANGYZ_pick_up@4PX.COM","post_code":"518000","country":"CN","state":"state_pick_up","city":"city_pick_up","district":"district_pick_up","street":"street_pick_up","house_number":"20"}},"express_to_4px_info":{"express_company":"4PXexpress_company","tracking_no":"8956232323"},"self_send_to_4px_info":{"booking_earliest_time":"1432710115000","booking_latest_time":"1432710115000"}},"label_config_info":{"label_size":"label_80x90","response_label_format":"PDF","create_logistics_label":"Y","logistics_label_config":{"is_print_time":"N","is_print_buyer_id":"N","is_print_pick_info":"N"},"create_package_label":"Y"},"order_attachment_info":[{}]}'

# 构建签名字符串（按照HTML工具的格式）
sign_str = "app_key" + APP_KEY + "formatjson" + "method" + "ds.xms.order.create" + "timestamp" + HTML_TIMESTAMP + "v" + "1.1.0" + HTML_JSON + APP_SECRET

# 计算MD5签名
python_sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()

print("=" * 70)
print("签名算法验证")
print("=" * 70)
print(f"\nHTML工具签名: {HTML_SIGN}")
print(f"Python签名:   {python_sign}")
print(f"\n签名是否匹配: {'✅ 匹配!' if python_sign == HTML_SIGN else '❌ 不匹配'}")

if python_sign != HTML_SIGN:
    print("\n" + "=" * 70)
    print("签名字符串对比（前200字符）:")
    print("=" * 70)
    print(f"Sign String: {sign_str[:200]}...")
    
    # 检查JSON差异
    print("\n检查JSON格式...")
    try:
        parsed = json.loads(HTML_JSON)
        regenerated = json.dumps(parsed, ensure_ascii=False, separators=(',', ':'))
        print(f"HTML JSON长度: {len(HTML_JSON)}")
        print(f"Regenerated长度: {len(regenerated)}")
        print(f"JSON是否一致: {'✅' if HTML_JSON == regenerated else '❌'}")
        
        if HTML_JSON != regenerated:
            # 找出第一个不同的字符
            for i, (c1, c2) in enumerate(zip(HTML_JSON, regenerated)):
                if c1 != c2:
                    print(f"第一个差异位置: {i}")
                    print(f"HTML: ...{HTML_JSON[max(0,i-10):i+10]}...")
                    print(f"Python: ...{regenerated[max(0,i-10):i+10]}...")
                    break
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
