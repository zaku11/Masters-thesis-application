public class Simple {
  public int f() {
    int y = x + 21;
    return 42;
  }
  public void g() {
    x++;
  }
  public void h() {
    int x = x + 1;
  }
  public int i() {
    int x = 42;
    return this.x;
  }
  public void j() {
    this.x++;
  }
  public void k() {
    --this.x;
  }
  public void l() {
    --x;
  }
  int x = f();
}
