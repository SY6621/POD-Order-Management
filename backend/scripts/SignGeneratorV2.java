import com.fpx.api.model.AffterentParam;
import com.fpx.api.utils.SignUtil;
import java.util.Map;
import java.util.HashMap;

/**
 * 4PX Sign Generator V2
 * 使用 AffterentParam 对象生成签名（与在线调试一致）
 */
public class SignGeneratorV2 {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: java SignGeneratorV2 <timestamp> <biz_content> [app_key] [app_secret]");
            System.exit(1);
        }

        String timestamp = args[0];
        String bodyJson = args[1];
        String appKey = args.length > 2 ? args[2] : "6efa9a05-5e31-4d2a-9a9c-da7624627f26";
        String appSecret = args.length > 3 ? args[3] : "0b768497-0c7a-4247-a7c0-0ca20cb2ae16";

        try {
            // 创建 AffterentParam 对象
            AffterentParam param = new AffterentParam();
            param.setAppKey(appKey);
            param.setAppSecret(appSecret);
            param.setFormat("json");
            param.setMethod("ds.xms.order.create");
            param.setVersion("1.1.0");
            param.setLanguage("cn");
            
            // 使用 getSingByParam 方法生成签名
            String sign = SignUtil.getSingByParam(param, bodyJson, Long.parseLong(timestamp));
            System.out.println(sign);
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
