### Rust Result Handling
- https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html

### Rust to String
- would like to convert objects to string
```rust
#[derive(Debug)]
struct A {
    names: Vec<String>,
}

fn main() {
    let a = A { names: vec![
        "Victor".to_string(),
        "Paul".to_string(),
    ]};
    // {:?} is used for debug
    println!("{:?}", a);
}
```
