# Datetime

## datetime cheat sheet

### From naive to aware, and show in different timezone
- !!The naming of the `datetime.replace(tzinfo = ...)` function is unfortunate. In fact, its behaviour is random. Do not use this!!!
```python
fullfmt = "%Y%m%d-%H:%M:%S %Z"
d3 = datetime.strptime("20230215-14:25:00 GMT", fullfmt)
print(d3.tzinfo) # None ... e.g. GMT isn't valid, the datetime is naive

#from pytz import timezone
import pytz

hktz = pytz.timezone('Asia/Hong_Kong')
d4 = hktz.localize(d3)
print(d4.tzinfo) # Correct way to make naive time to be aware!!!
print(d4.strftime(fullfmt))

eastern = pytz.timezone('US/Eastern')
print(d4.astimezone(eastern).strftime(fullfmt))
```


## Timezone aware or not
- Date and time objects may be categorized as **“aware” or “naive”** depending on whether or not they include timezone information.
- With sufficient knowledge of applicable algorithmic and political time adjustments, such as time zone and daylight saving time information, an **aware object can locate itself relative to other aware objects.**
- **An aware object** represents a **specific moment** in time that is not open to interpretation.

- A naive object does **not contain enough** information to unambiguously locate itself relative to other date/time objects.
- Whether a naive object represents Coordinated Universal Time (UTC), local time, or time in some other timezone is purely up to the program, just like it is up to the program whether a particular number represents metres, miles, or mass.
- Naive objects are easy to understand and to work with, at the cost of **ignoring some aspects of reality**.

- For applications requiring aware objects, **datetime and time objects have an optional time zone information attribute,** `tzinfo`, that can be set to an instance of a subclass of the abstract tzinfo class.
- These tzinfo objects capture information about the offset from UTC time, the time zone name, and whether daylight saving time is in effect.

- Only one concrete `tzinfo` class, the `timezone` class, is supplied by the datetime module.
  - The timezone class can represent** simple timezones with fixed offsets from UTC**, such as UTC itself or North American EST and EDT timezones.
  - Supporting `timezones` at deeper levels of detail is up to the application.
  - The rules for time adjustment across the world are more political than rational, change frequently, and there is no standard suitable for every application **aside from UTC.**


## Subclass relationship
```txt
time
date
    \datetime
tzinfo
    \timezone
timedelta
```
- `datetime.time`:
  - An idealized time, **independent of any particular day**, assuming that every day has exactly 24*60*60 seconds. (There is no notion of “leap seconds” here.) Attributes: hour, minute, second, microsecond, and **tzinfo**.
- `datetime.date`:
  - An idealized **naive** date, assuming the current Gregorian calendar always was, and always will be, in effect. Attributes: year, month, and day.
- `datetime.datetime`:
  - A combination of a date and a time. Attributes: year, month, day, hour, minute, second, **microsecond**, and **tzinfo**.
- `datetime.tzinfo`:
  - An abstract base class for time zone information objects.
  - These are used **by the `datetime` and `time` classes** to provide a customizable notion of `time` adjustment
  - (for example, to account for time zone and/or daylight saving time).
- `datetime.timezone`:
  - A class that implements the tzinfo abstract base class as a fixed offset from the UTC.
- `datetime.timedelta`:
  - A duration expressing the difference between two `date`, `time`, or `datetime` instances **to microsecond resolution.**

## Determining if an Object is Aware or Naive
- Objects of the `date` type are always naive.
  - An object of type `time` or `datetime` may be aware or naive.
- A `datetime` object `d` is aware if both of the following hold:
  - `d.tzinfo` is not None
  - `d.tzinfo.utcoffset(d)` does not return `None`
  - Otherwise, `d` is naive.
- A `time` object `t` is aware if both of the following hold:
  - `t.tzinfo` is not `None`
  - `t.tzinfo.utcoffset(None)` does not return `None`.
  - Otherwise, `t` is naive.
- The distinction between aware and naive doesn’t apply to `timedelta` objects.
