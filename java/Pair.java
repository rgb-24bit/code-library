import java.util.Objects;

/**
 * Container to ease passing around a tuple of two objects. This object provides a sensible
 * implementation of equals(), returning true if equals() is true on each of the contained
 * objects.
 */
public class Pair<L, R> {
  public final L left;
  public final R right;

  /**
   * Constructor for a Pair.
   *
   * @param left the left object in the Pair
   * @param right the right object in the pair
   */
  public Pair(L left, R right) {
    this.left = left;
    this.right = right;
  }

  /**
   * Checks the two objects for equality by delegating to their respective
   * {@link Object#equals(Object)} methods.
   *
   * @param o the {@link Pair} to which this one is to be checked for equality
   * @return true if the underlying objects of the Pair are both considered
   *         equal
   */
  @Override
  public boolean equals(Object o) {
    if (!(o instanceof Pair)) {
      return false;
    }
    Pair<?, ?> p = (Pair<?, ?>) o;
    return Objects.equals(p.left, left) && Objects.equals(p.right, right);
  }

  /**
   * Compute a hash code using the hash codes of the underlying objects
   *
   * @return a hashcode of the Pair
   */
  @Override
  public int hashCode() {
    return (left == null ? 0 : left.hashCode()) ^ (right == null ? 0 : right.hashCode());
  }

  @Override
  public String toString() {
    return "Pair{" + String.valueOf(left) + " " + String.valueOf(right) + "}";
  }

  /**
   * Convenience method for creating an appropriately typed pair.
   * @param a the left object in the Pair
   * @param b the right object in the pair
   * @return a Pair that is templatized with the types of a and b
   */
  public static <A, B> Pair <A, B> create(A a, B b) {
    return new Pair<A, B>(a, b);
  }
}
