public interface Omitting {
    default void foo() {
        self.x++;
        self.y++;
    }
    void bar();
}
public enum Omitting2 {
    F("foo"),
    B("bar");

    public final String label;

    private void set() {
        this.label = "123";
    }
}