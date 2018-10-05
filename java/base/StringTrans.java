import java.util.HashMap;
import java.util.Map;

/**
 * Java porting of the translate method of strings in Python.
 */
public class StringTrans {
  private Map<Character, Character> trans;

  /**
   * You should create an instance using the {@link #maketrans(String, String) maketrans} method.
   * @param intab The string of characters to be replaced in the string.
   * @param outtab Corresponding string of mapped characters.
   */
  private StringTrans(String intab, String outtab) {
    trans = new HashMap<Character, Character>();

    for (int i = 0; i < intab.length(); ++i) {
      trans.put(intab.charAt(i), outtab.charAt(i));
    }
  }

  /**
   * Create a StringTrans instance. The length of the incoming parameters must be equal.
   * @param intab The string of characters to be replaced in the string.
   * @param outtab Corresponding string of mapped characters.
   * @return StringTrans instance.
   * @throws IllegalArgumentException If the parameter lengths are not equal.
   */
  public static StringTrans maketrans(String intab, String outtab) {
    if (intab.length() != outtab.length()) {
      throw new IllegalArgumentException("The length of the two parameters must be equal.");
    }
    return new StringTrans(intab, outtab);
  }

  /**
   * Return a copy of the string origin in its each character has been mapped.
   * @param origin The string to be translated.
   * @return Translated string.
   */
  public String translate(String origin) {
    StringBuilder sb = new StringBuilder(origin.length());

    for (int i = 0; i < origin.length(); ++i) {
      sb.append(trans.getOrDefault(origin.charAt(i), origin.charAt(i)));
    }

    return sb.toString();
  }
}
