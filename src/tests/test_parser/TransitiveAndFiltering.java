public class Father {
  int a;
  public void foo() {}
}

public class TransitiveAndFiltering extends Father {
  public int sum() {
    return x + a;
  }
  public void invoker() {
    sum();
    foo();
    someRandomThing.invoker();
  }
  public void rec() {
    this.rec();
    x++;
    // y++;
  }

  int x;
  int y;
  int z;
}