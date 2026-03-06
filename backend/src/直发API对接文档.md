# 正式环境请求协议建议升级到https

直发接口链接：[http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=96](http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=96)

请求地址:

|   |   |
|---|---|
|环境|HTTP请求地址|
|正式环境|https://open.4px.com/router/api/service|
|测试环境|https://open-test.4px.com/router/api/service|

# 介绍：

## 一、API接口流程图

**递四方商户接入：**

- [ ] **注：***如调用的测试环境不需要申请账号与APP，请使用我们提供的APP**
- [ ] 测试环境：**AppKey：****5dca6db7-6a21-4d31-a5f8-33a24a4f5b9d**
- [ ] 测试环境：**AppSecrt：****b8bd24a5-35b0-4e8a-bbc0-c7458e21c7ad**

**递四方软件服务商接入：**

- [ ] **注：****如调用的测试环境不需要申请商家账号，软件服务商账号（合作伙伴），商家账号请使用我们提供的（如你属于软件服务商，需要测试环境的商家账号，请联系4PX技术支持）。**
- [ ] 测试环境账号密码，商家与软件服务商同一个账号密码 账号18820295523 密码 fpx@123456

### 1.调用API接口前确认
[[b7184c458b74a02c8359582532f815cb_MD5.jpg|Open: Pasted image 20260304114405.png]]
![[b7184c458b74a02c8359582532f815cb_MD5.jpg]]
### 2.API接口流程图（参考）

[[ac4e6d89b64c5aa97c491d64d0780d47_MD5.jpg|Open: Pasted image 20260304114430.png]]
![[ac4e6d89b64c5aa97c491d64d0780d47_MD5.jpg]]
## 二、主要接口讲解

### 1.ds.xms.order.create(创建直发委托单)

版本号：1.1.0

接口文档：[http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=96](http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=96)

#### (1)(简单)请求示例：

```
//API接口文档，每个都有注释，可查看
{
    "ref_no":"TEST-1234567",//每个走货账号下-客户单号保持唯一
    "business_type":"BDS",//直发业务类型 BDS
    "duty_type":"P",//税费费用承担方式,可以咨询我们业务了解
    "vat_no":"",//VAT税号,如发的欧盟有IOSS号可不填
    "eori_no":"",//欧盟入关时需要EORI号码，用于商品货物的清关,欧盟有传IOSS号可不填,非欧盟不用填
    "ioss_no":"IM0123456789",//欧盟税改 IOSS号
    "parcel_qty":"",//包裹件数（一个订单有多少件包裹，就填写多少件数，请如实填写包裹件数，
                    //否则DHL无法返回准确的子单号数和子单号标签；DHL产品必填，如产品代码A1/A5；）
    "freight_charges":"",//运费(客户填写自己估算的运输费用；支持的币种，根据物流产品+收件人国家配置)
    "currency_freight":"",//运费币种(按照ISO标准三字码；支持的币种，根据物流产品+收件人国家配置)
    "declare_insurance":"",//申报保险费（是否必填，根据物流产品+目的国配置；根据欧盟IOSS政策，
                           //货值/运费/保险费可单独申报）支持小数点后2位
    "currency_declare_insurance":"",//申报保险费币种（按照ISO标准，币种需和进出口国申报币种一致）
    "logistics_service_info":{
        "logistics_product_code":"PY" //产品渠道代码,可以调用物流产品接口获取所有可走货产品
    },
    "return_info":{//退件信息
      //退件地址可不填，如果要填这几个字段都要填，
      //要么一个不填姓名/电话/邮编/国家/城市/详细地址
        "is_return_on_domestic":"Y",//境内退件 Y 退件  N 销毁 U 其他
        "is_return_on_oversea":"Y" //境外退件
      //注：目前系统判断 是否退件   Y：退件（否）  N/U：不退件（否）
      //最终此渠道是否退件可以咨询我们业务了解
    },
    "parcel_list":[//包裹列表
        {
            "weight":169,//预报重，单位g克，不能有小数
            "parcel_value":9,//申报总价值=申报单价X申报数量
            "currency":"USD",//申报币种，非欧盟国家目前币种都是USD ，欧盟国家支持EUR 
             //如果报错不支持USD，先看是不是发的欧盟，如发的欧盟就改成EUR
             //特别注意,货币类型换了后对应的数值也要换算
             //货币类型保持一致，比如走欧洲的只支持欧元，所有的货币类型都要保持一致
            "include_battery":"N",//是否带电，N否
            //如传带电Y就要传电池类型，如电池类型不传,到我们系统就是默认的电池类型
          //电池类型对应表，请看上面动态，具体可以选哪些电池类型可以咨询我们业务
            //"product_list":{ //商品信息-(可以不传)
            //   "product_name":"猫碗",//商品名称
            //    "product_description":"bowl",//商品描述
             //   "product_unit_price":8.29,//商品单价
             //   "currency":"USD",//商品货币类型（和实际支持的货币类型保持一致）
            //    "qty":"1" //商品数量
          //  },
          //申报总价值=申报单价X数量   注意：申报单价，只取百分位,四舍五入
            "declare_product_info":[{//海关申报品
                "declare_product_name_cn":"猫碗",//中文申报品名,必须至少包要含一个中文
                "declare_product_name_en":"bowl",//英文申报品名，不能包含中文，及特殊符号
                "declare_product_code_qty":"1",//申报数量
                "declare_unit_price_export":9,//出口申报单价（目前建议进出口申报单价传一样）
                "currency_export":"USD",//出口货币类型，货币类型保持一致
                "declare_unit_price_import":9,//进口申报单价（目前建议进出口申报单价传一样）
                "currency_import":"USD",//进口货币类型,货币类型保持一致
                "brand_export":"无",//出口品牌，如无可以填空""
                "brand_import":"无",//进口品牌，如无可以填空""
                "hscode_export":"",//出口海关编码，如是必填的，进出口保持一致
                "hscode_import":"",//进口海关编码，如是必填的，进出口保持一致
                "uses":"YONGTU",//用途   dhl 联邦渠道需要传英文涉及产品A1 A5 E4 E5 E6 E7 （值：必须英文）
                "material":"CAIZHI",//材质  dhl 联邦渠道需要传英文涉及产品A1 A5 E4 E5 E6 E7（值：必须英文）
              //材质用途这2个字段，非联邦DHL产品渠道的建议不要传，如要传一定要英文
                "package_remarks":"配货信息"//如填了后可以打印在面单上
            }]
        }
    ],
    "is_insure":"Y",//是否投保，这个是购买4PX的保险,货币类型必须是USD，和其他申报品货币类型不关联
    "insurance_info":{
        "insure_type":"5Y",// 保险类型，保险类型（XY:4PX保价；XP:第三方保险） 5Y, 5元每票 8Y, 8元每票 6P, 0.6%保费
        "insure_value":"23",//保险价值，相关的4PX保险购买可以咨询我们业务了解
        "currency":"USD"//保险币别 ，4PX保险必须是USD
    },
    "sender":{ //发件人信息
        "first_name":"Wu Rao",//发件人姓名。可以直接传在这个字段里
        "company":"4PX",//发件人公司
        "phone":"13000000000",//发件人手机电话
        "post_code":"123456",//发件人邮编
        "country":"CN",//发件人国家/地区
        "state":"GuangDong",//发件人省份
        "city":"Shengzhen",//发件人城市
        "street":"caifugang 4PX 25-26"//发件人详细地址
    },
    "recipient_info":{//收件人信息
        "first_name":"zhang san",//收件人姓名
        "phone":"1234567890",//收件人电话
        "post_code":"13021",//收件人邮编
        "country":"US",//收件人国家
        "state":"NY",//New York 如果洲省有缩写的,可以填入缩写
        "city":"Auburn",//收件人城市
        "street":"str 123",//收件人详细地址,
        "house_number":"",//收件人门牌号
      //【只适用DHL到德国的渠道：如门牌号没填值,但详细地址有门牌号，可单独用空格分开，我们会抓取作为门牌号】
        "email":""//收件人邮箱
    },
    "deliver_type_info":{//到仓方式,可以找我们业务了解
        "deliver_type":"1"//到仓方式（1:上门揽收；2:快递到仓；3:自送到仓；5:自送门店）
    }
}
```

(2)注意

以下单响应的单号最好能展示出来，如出现报错，自己无法排查，可以反馈给我们,快速定位问题.

下单时不要让连续请求点击，如需再次请求，请等系统响应成功后再根据实际情况是否再做二次请求

|   |   |   |
|---|---|---|
|响应参数|**示例值**|**描述**|
|ref_no|TEST-1234567|客户单号（参考号）|
|4px_tracking_no|300900010807|4PX单号（可以查看预报到出库发货前的头程轨迹）|
|logistics_channel_no|84355123456789|服务商单号，一般提供给平台或客户的，查询尾程轨迹（如果结果返回为空字符，表示暂时没有物流渠道号码，请稍后主动调用查询直发委托单接口查询）|

### 2.ds.xms.order.get(查询直发委托单)

版本号：1.1.0

接口文档：[http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=98](http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=98)

(1)注意

1.调用查询接口，只支持4PX单号和客户单号请求。

2.详情看此文档说明：

[https://4pxgroup.yuque.com/docs/share/e957c444-eb33-48ac-ab0e-ce1209424045?#](https://4pxgroup.yuque.com/docs/share/e957c444-eb33-48ac-ab0e-ce1209424045?#) 《直发API 查询接口(取号标识-取号报错说明)》

### 3.ds.xms.order.cancel(取消直发委托单)

版本号：1.0.0

接口文档：[http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=99](http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=99)

(1)注意

1.调用此接口，只支持4PX单号和客户单号请求。

2.如果已经下单成功的订单（不管有没有成功获取服务商单号，只要调用查询接口能查询到的），如需要修改订单信息，必须先取消我们4PX系统的这单，然后再调用接口请求（如果不取消会报，此单已存在就是这个原因了）

### 4.ds.xms.label.get(获取标签)

版本号：1.1.0

接口文档：[http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=102](http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=102)

(1)注意

1.调用标签接口，支持客户单号和4PX单号和服务商单号请求。

2.label_size 标签大小 传值 label_100x150 一般我们分为10*10的面单（CM）10*15的面单（CM）

3.这个接口会默认出面单本来的大小,建议传参填写正确的参数

4.is_print_merge 如果报关单和配货单报关单要合并在一个PDF连接里，这个值需要传Y，其他的如是否打印配货单，报关单也需要传Y，才会合并。

5.is_print_pick_info 是否打印配货信息到面单上（由创建订单parcel_list>declare_product_info>create_package_label字段控制）如配货信息字段有传值，面单上就可以显示配货信息（是否打印配货信息，只能控制4PX通用/普通标签是否显示，如一体化标签/服务商标签无法控制， 配货信息填了就会显示，如不想显示，下单时不要传配货信息）

6.相关参数具体看接口文档

### 5.ds.xms.label.getlist(批量获取标签)

版本号：1.0.0

接口文档：[http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=165](http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=165)

(1)注意

1.调用标签接口，支持客户单号和4PX单号和服务商单号请求。

2.批量接口打印的面单默认合并在一个PDF链接里。

3.如需要10*15的面单和10*10的面单一起打印，大小需要传 label_100x150 才可以

4.相关参数具体看接口文档

  

### 6.ds.xms.logistics_product.getlist(物流产品查询)

版本号：1.0.0

接口文档：[http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=167](http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=167)

1.这个接口，主要是实时获取4PX的物流产品渠道，能走货的渠道才能查询出来，已关闭的渠道是不会显示的，这个对接上，避免后期不必要的维护

### 7.ds.xms.order.updateweight(更新预报重)

版本号：1.0.0

接口文档：[http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=169](http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=169)

1.更新预报重（只有已预报且未到仓的包裹订单，能更新预报重）

2.调用查询接口，支持4PX单号和客户单号，服务商单号请求。

3.只支持生产环境调用此接口，如只修改预报状态的订单就不需要取消重新预报了

  

### 8.tr.order.tracking.get(物流轨迹查询)

版本号：1.0.0

接口文档：[http://open.4px.com/apiInfo/apiDetail?itemId=6&mainId=25](http://open.4px.com/apiInfo/apiDetail?itemId=6&mainId=25)

4PX轨迹官网：[http://track.4px.com/#/](http://track.4px.com/#/)

1.根据自身情况是否要对接轨迹接口

2.调用轨迹接口，只支持4PX单号和服务商单号请求。

3.只支持生产环境调用轨迹接口，请在生产环境调试，如果需要已出库的单号找我们4PX业务提供

  

### 9.ds.xms.estimated_cost.get(预估费用查询/运费试算)

版本号：1.0.0

接口文档：[http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=181](http://open.4px.com/apiInfo/apiDetail?itemId=2&mainId=181)

1.根据自身情况是否要对接运费试算接口

2.只支持生产环境调用此接口

### 10.注意

以上接口1-6请求的都比较常用的，建议一定要对接上,6-9根据自身情况对接(一般软件服务商都是有对接的)。