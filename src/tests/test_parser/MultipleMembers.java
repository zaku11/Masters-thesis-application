public class FatherOne {
  int a;
}
public class FatherTwo extends FatherOne {
  int b;
}

public class MultipleMembers extends FatherTwo {
  public int sumFirst() {
      return x + this.y;
  }
  public int sumSecond() {
      return sumFirst() + z;
  }
  public int sum(int x, int y) {
    return x + y + a + b;
  }
  int x;
  int y;
  int z;
}