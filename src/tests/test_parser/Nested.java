class OuterClass {
    int x;
    void foo() {
        this.x++;
    }
    void bar() {}

    class NestedClass {
        int y;
        void foobar() {
            this.y++;
        }
        void barfoo() {}
    }
}