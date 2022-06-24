public class Test {
  void g() {
    this.foo.x += 1;
  }
  void fake() {
    foo(123);
  }
  void g2() {
    this.foo.x++;
  }
  void g3() {
    this.fun(this.foo);
  }
  void g4() {
    fun(foo);
  }
  void g5() {
    fun(foo.abc);
  }
  something foo;
}
