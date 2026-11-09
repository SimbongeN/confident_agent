interface InputDevice { void input(); }
class Keyboard implements InputDevice {
    public void input() { /* ... */ }
}
class Computer {
    private final InputDevice device;
    Computer(InputDevice device) { this.device = device; }
    void type() { device.input(); }
}