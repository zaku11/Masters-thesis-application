public class Stuff {
  public int f(int x) {
    return 42;
  }
  public void g() {
    int c = f(42);
  }
  public int foo(int x) {
    return 42;
  }
  public void goo() {
    int c = foo(((10 + 10) / 3));
  }
  public void goo2() {
    int c = this.foo(((10 + 10) / 3));
  }
  public void goo3() {
    int c = fun(((10 + foo(10)) / 3));
  }
  public void goo4() {
    int c = fun(((10 + fun(10)) / this.foo(3)));
  }  
  public void somethingElse1() {
    int c = this.f(((10 + this.foo(10)) / 1));
  }  
  public void somethingElse2() {
    int c = fun(((10 + this.foo(10)) / this.f(1)));
  }  
  public void somethingElse3() {
    int c = fun(((10 + foo(10)) / this.f(1)));
  }  
  public void somethingElse4() {
    int c = fun(((10 + foo(10)) / f(1)));
  }  
  public void somethingElse5() {
    int c = this.f(foo(10));
  }  
}
