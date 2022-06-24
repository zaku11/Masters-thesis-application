public class Test {
  void getX() {
    return x;
  }
  void getx() {
    return x;
  }
  void setX(int z) {
    x = z;
  }
  void setx(int z) {
    x = z;
  }
  void foo() {
    getX();
    getx();
    setX();
    setx();
  }  
  void getZ() {
    y += 1;
  }
  int x;
  int y;
}