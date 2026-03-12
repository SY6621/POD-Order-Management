"""
创建 Java Wrapper 来调用 4PX SDK

由于直接反编译没有成功，我们创建一个简单的 Java 程序来调用 SDK，
然后通过命令行与 Python 交互
"""

java_code = '''
import com.fpx.api.model.AffterentParam;
import com.fpx.api.utils.SignUtil;

public class TestSign {
    public static void main(String[] args) {
        String appKey = "6efa9a05-5e31-4d2a-9a9c-da7624627f26";
        String appSecret = "0b768497-0c7a-4247-a7c0-0ca20cb2ae16";
        String format = "json";
        String method = "ds.xms.order.create";
        String timestamp = args[0];  // 从命令行传入
        String version = "1.1.0";
        String bodyJson = args[1];   // 从命令行传入
        
        String sign = SignUtil.getSign(appKey, format, method, timestamp, version, bodyJson, appSecret);
        System.out.println("SIGN:" + sign);
    }
}
'''

print("=" * 60)
print("Java Wrapper 代码")
print("=" * 60)
print(java_code)

print("\n" + "=" * 60)
print("使用说明")
print("=" * 60)
print("""
要使用这个方案，需要：
1. 安装 Java JDK
2. 编译上述 Java 代码
3. 运行 Java 程序获取签名

编译命令：
javac -cp fpx-api-sdk-1.0.0-SNAPSHOT.jar TestSign.java

运行命令：
java -cp .;fpx-api-sdk-1.0.0-SNAPSHOT.jar TestSign <timestamp> <biz_content>

但由于 Java 未安装，此方案暂时无法使用。
""")
