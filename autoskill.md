# Robot Skills

> ARF 机器人能力描述文档
> Hermes Agent 通过此文档理解机器人能力

---

## walk

### Description
Control robot movement in different directions.

### Input Parameters
- **speed** (float): Movement speed, range [-1.0, 1.0], default 0.5
- **direction** (string): Movement direction, options: forward, backward, left, right
- **duration** (float): Duration in seconds, range [0.0, 60.0], default 5.0

### Output
- **success** (bool): Execution result
- **distance** (float): Distance traveled in meters

### Example Usage
```
walk speed=0.5 direction=forward duration=5.0
walk speed=0.3 direction=backward duration=3.0
walk speed=0.4 direction=left duration=2.0
```

### Permission Required
- motor
- navigation

---

## stop

### Description
Stop all robot movements immediately.

### Input Parameters
None

### Output
- **success** (bool): Stop result

### Example Usage
```
stop
```

### Permission Required
- motor

---

## Future Skills

- **sit**: Make robot sit down
- **stand**: Make robot stand up
- **follow**: Follow a target
- **grasp**: Grasp an object
- **dance**: Perform dance movements
