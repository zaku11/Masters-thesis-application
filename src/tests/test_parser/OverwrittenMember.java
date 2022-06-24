public class OverwrittenMember {
  public void f(int p) {
    int x = 12;
    int y = x + 21;
  }
  public void g(int x) {
    x++;
  }
  int x = 5;
}