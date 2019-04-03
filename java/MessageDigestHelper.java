import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * Help with a digest of the message.
 */
public class MessageDigestHelper {
  /**
   * MD5 digest on the specified string and return the hex digest string.
   * @param input The string to be MD5 digest.
   * @param charsetName Coded character set of a string.
   * @return Hex digest string. Error returning null.
   */
  public static String md5(String input, String charsetName) {
    try {
      MessageDigest md5 = MessageDigest.getInstance("MD5");
      md5.update(input.getBytes(charsetName));
      return formatDigest(md5.digest());
    } catch (NoSuchAlgorithmException | IOException e) {
      e.printStackTrace();
    }
    return null;
  }

  /**
   * MD5 digest on the specified string and return the hex digest string.
   * @param input The string to be MD5 digest.
   * @return Hex digest string.
   */
  public static String md5(String input) {
    try {
      MessageDigest md5 = MessageDigest.getInstance("MD5");
      md5.update(input.getBytes());
      return formatDigest(md5.digest());
    } catch (NoSuchAlgorithmException e) {
      e.printStackTrace();
    }
    return null;
  }

  /**
   * SHA-1 digest on the specified string and return the hex digest string.
   * @param input The string to be SHA-1 digest.
   * @param charsetName Coded character set of a string.
   * @return  Hex digest string. Error returning null.
   */
  public static String sha1(String input, String charsetName) {
    try {
      MessageDigest sha1 = MessageDigest.getInstance("SHA-1");
      sha1.update(input.getBytes(charsetName));
      return formatDigest(sha1.digest());
    } catch (NoSuchAlgorithmException | IOException e) {
      e.printStackTrace();
    }
    return null;
  }

  /**
   * SHA-1 digest on the specified string and return the hex digest string.
   * @param input The string to be SHA-1 digest.
   * @return Hex digest string.
   */
  public static String sha1(String input) {
    try {
      MessageDigest sha1 = MessageDigest.getInstance("SHA-1");
      sha1.update(input.getBytes());
      return formatDigest(sha1.digest());
    } catch (NoSuchAlgorithmException e) {
      e.printStackTrace();
    }
    return null;
  }

  /**
   * SHA-256 digest on the specified string and return the hex digest string.
   * @param input The string to be SHA-256 digest.
   * @param charsetName Coded character set of a string.
   * @return  Hex digest string. Error returning null.
   */
  public static String sha256(String input, String charsetName) {
    try {
      MessageDigest sha256 = MessageDigest.getInstance("SHA-256");
      sha256.update(input.getBytes(charsetName));
      return formatDigest(sha256.digest());
    } catch (NoSuchAlgorithmException | IOException e) {
      e.printStackTrace();
    }
    return null;
  }

  /**
   * SHA-256 digest on the specified string and return the hex digest string.
   * @param input The string to be SHA-256 digest.
   * @return Hex digest string.
   */
  public static String sha256(String input) {
    try {
      MessageDigest sha256 = MessageDigest.getInstance("SHA-256");
      sha256.update(input.getBytes());
      return formatDigest(sha256.digest());
    } catch (NoSuchAlgorithmException e) {
      e.printStackTrace();
    }
    return null;
  }

  /**
   * Formatted digest information as a lower case hexadecimal string format.
   * @param bytes digest information.
   * @return Hex digest string.
   */
  private static String formatDigest(byte[] bytes) {
    StringBuilder sb = new StringBuilder();

    for (int i = 0; i < bytes.length; ++i) {
      sb.append(String.format("%02x", bytes[i]));
    }

    return sb.toString();
  }
}
