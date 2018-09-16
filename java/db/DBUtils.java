import java.sql.*;

/**
 * Database utils class, provides access to database connections and closed connections.
 */
public class DBUtils {
  private static final String url = "";
  private static final String user = "";
  private static final String password = "";
  private static final String driver = "";

  /**
   * This class not instance.
   */
  protected DBUtils() {}

  /**
   * Try to get a sql.Connection object.
   *
   * @return A sql.Connection object.
   * @throws ClassNotFoundException if the driver not found.
   * @throws SQLException           if get connection error.
   */
  public static Connection getConnection() throws ClassNotFoundException, SQLException {
    Class.forName(driver);
    return DriverManager.getConnection(url, user, password);
  }

  /**
   * Close Connection object.
   * @param connection Connection object.
   */
  public static void close(Connection connection) {
    if (connection != null) {
      try {
        connection.close();
      } catch (SQLException ex) {
        ex.printStackTrace();
      }
    }
  }

  /**
   * Close PreparedStatement object.
   * @param connection PreparedStatement object
   */
  public static void close(PreparedStatement connection) {
    if (connection != null) {
      try {
        connection.close();
      } catch (SQLException ex) {
        ex.printStackTrace();
      }
    }
  }

  /**
   * Close ResultSet object.
   * @param connection ResultSet object.
   */
  public static void close(ResultSet connection) {
    if (connection != null) {
      try {
        connection.close();
      } catch (SQLException ex) {
        ex.printStackTrace();
      }
    }
  }
}
