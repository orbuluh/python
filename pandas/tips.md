# 1. Show installed versions
```python
pd.__version__
# also show dependencies
pd.show_versions()
```

## 2. Create an example DataFrame
```python
pd.DataFrame({'col one':[100, 200], 'col two':[300, 400]})
pd.DataFrame(np.random.rand(4, 8))
pd.DataFrame(np.random.rand(4, 8), columns=list('abcdefgh'))
```

# 3. Rename columns
```python
df = df.rename({'col one':'col_1', 'col two':'col_2'}, axis='columns')
# if you want to rename all columns, use:
df.columns = ['col_one', 'col_two']
df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.replace('_', '-')
df = df.add_prefix('Oo_')
df = df.add_suffix('_oO')
```


