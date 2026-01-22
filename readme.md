# kungfu

⚙️ Functional typing in Python!

```python
get_user()
  .then(get_posts)
  .ensure(lambda posts: len(posts) > 0, "User has no posts")
  .map(lambda posts: sum(post.views for post in posts) / len(posts))
  .unwrap()
```

## why kungfu?

kungfu is based on the belief that raising exceptions should be avoided. So it defines a set of functional types needed to write better code. This type strategy grants you with higher control over your runtime.

Panicking is the last recourse but for some obscure reason spawning exceptions each time you encounter something other than the all-successful behaviour became a norm in python code.

Let's fix this up and instead of panicking do treat error-state as equal to successful-state. kungfu provides you with all you need to migrate to functional typing approach

Improving control flow will definitely result in avoiding logical errors and getting better code readability: you start to see each kind of behaviour you get from the function.

why "kungfu" as a name? writing in kungfu requires some discipline. kung fu literally meaning "hard work" reflects on this concept. through the hard work on gaining control over our types we get clarity and power

## (📖) documentation

See [documentation](/docs/index.md)

See [examples](/examples/)

## examples

**howto** build monad chains:

```python
def get_user(user_id: int) -> Result[User, str]:
    ...

def get_posts(user: User) -> Result[list[Post], str]:
    ...

def get_average_views(user_id: int) -> Result[int, str]:
    return (
        get_user(user_id)
        .then(get_posts)
        .ensure(len, "User has no posts")
        .map(lambda posts: sum(post.views for post in posts) / len(posts))
    )

avg_views = get_average_views().unwrap()
```

**howto** detalize function result:

```python
@unwrapping
def send_funds(
    sender_id: int, 
    receiver_id: int, 
    amount: decimal.Decimal,
) -> Result[TransactionID, str]:
    sender = get_user(sender_id).expect("Sender is undefined")
    receiver = get_user(receiver_id).expect("Receiver is undefined")

    if sender.get_balance().expect("Could not get sender balance") < amount:
        return Error("Sender has not enough funds to complete transaction")
    
    return Ok(
        create_transaction(sender, receiver, amount)
        .unwrap()
        .transaction_id
    )
```

## install

```sh
pip install kungfu-fp
```

Contributions are welcome

MIT licensed

---

# awesome kungfu projects

[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

These projects are awesome to extend kungfu environment:

* **[nodnod](https://github.com/timoniq/nodnod)** - dependency injection with efficient nodes computation agents and dependency scoping

* **[combinators.py](https://github.com/prostomarkeloff/combinators.py)** - build explicit functional pipelines

These projects implement kungfu environment in their specific utility cases:

* **[telegrinder](https://github.com/timoniq/telegrinder)** - telegram bot framework
