interface PaymentProcessor { void pay(double amount); }
class StripeProcessor implements PaymentProcessor {
    public void pay(double amount) { /* ... */ }
}
class OrderService {
    private final PaymentProcessor processor;
    OrderService(PaymentProcessor processor) { this.processor = processor; }
}