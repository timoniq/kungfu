# fntypes - Sum

`Sum` is a functional replacement for `Union` typehint. It has methods to enhance the control flow over union types. Some of these methods use head-tail notation due to the type-hinting restrictions.

Sum can contain multiple types (let the number of types be called N), therefore it can be contracted to N-1 states. Let's review the methods we can use to do so.

Head-tail notation is a notation that splits any set of data in two parts: head - the first element, and tail, that is a set of everything else. Therefore, if we consider a `Sum[A, B, C]`, its head will be `A`, and tail `[B, C]`.

## `.only(type = default to *head*)`

Only contracts the sum to a single type and returns a `Result[type, str]`

```python
x: Sum[A, B, C]

x.only(B) # Result[B, str]
x.only() # Result[A, str] (heading type of sum is A)
```

Now, when you understand the concept, the syntaxic replacement can be intruduced:

```python
x[B].expect("Can only be B")
# Can be used interchangably with
x.only(B).expect("Can only be B")
```

## `.detach()`

Head ensures that sum is not of *head* type and returns a result with a value-state of sum of *tail* types.

```python
x.detach()  # Result[Sum[B, C], str]
```

## `.v`

Returns a union (basically an intersection of all types of sum).

```python
x.v # Union[A, B, C]
```

