import io.kaitai.struct.*;

public class Main {

	public static void main(String[] args) {
		byte[] input = int2byte(new int[]{
				0xdd, 0x03, 0x00, 0x1b, 0x11, 0x38, 0x00, 0x62,
				0x00, 0xa4, 0x04, 0xb0, 0x00, 0x00, 0x27, 0x6e,
				0x02, 0x82, 0x00, 0x00, 0x00, 0x00, 0x21, 0x0e,
				0x03, 0x0b, 0x02, 0x0b, 0x22, 0x0b, 0x10, 0xfc,
				0x42, 0x77});
		BasicInfo info = new BasicInfo(new ByteBufferKaitaiStream(input));
		System.out.println(info.totalV());
		System.out.println(info.balanceStatus().flag());
		System.out.println("Charge"+ info.fetStatus().charge() + " Discharge" + info.fetStatus().charge());
		System.out.println(info.toString());
	}
	
	static byte[] int2byte(int[] in) {
		var out = new byte[in.length];
		for (int i = 0; i < in.length; i++) {
			out[i] = (byte) in[i];
		}
		return out;
	}

}
