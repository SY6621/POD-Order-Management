import com.fpx.api.model.AffterentParam;
import com.fpx.api.utils.SignUtil;

/**
 * 4PX Sign Generator
 * Used by Python to call Java SDK for generating correct signatures
 */
public class SignGenerator {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: java SignGenerator <timestamp> <biz_content> [app_key] [app_secret]");
            System.exit(1);
        }

        // Get values from command line args, or use defaults
        String timestamp = args[0];
        String bodyJson = args[1];
        String appKey = args.length > 2 ? args[2] : "6efa9a05-5e31-4d2a-9a9c-da7624627f26";
        String appSecret = args.length > 3 ? args[3] : "0b768497-0c7a-4247-a7c0-0ca20cb2ae16";

        String format = "json";
        String method = "ds.xms.order.create";
        String version = "1.1.0";

        try {
            // Use SDK to generate signature
            String sign = SignUtil.getSign(appKey, format, method, timestamp, version, bodyJson, appSecret);
            System.out.println(sign);
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
