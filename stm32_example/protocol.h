/**
 * ARF STM32 Protocol Header
 * STM32 协议定义
 */

#ifndef __ARF_PROTOCOL_H
#define __ARF_PROTOCOL_H

#include <stdint.h>
#include <stdbool.h>

/* 协议常量 */
#define FRAME_HEAD          0xAA55
#define PROTOCOL_VERSION    0x01
#define MAX_PAYLOAD_SIZE    256

/* 命令 ID */
typedef enum {
    /* Motor commands (0x01xx) */
    CMD_MOTOR_SET_SPEED     = 0x0101,
    CMD_MOTOR_SET_POSITION  = 0x0102,
    CMD_MOTOR_STOP          = 0x0103,
    CMD_MOTOR_SET_TORQUE    = 0x0104,
    CMD_MOTOR_GET_STATUS    = 0x0105,
    
    /* Servo commands (0x02xx) */
    CMD_SERVO_MOVE          = 0x0201,
    CMD_SERVO_ENABLE        = 0x0202,
    CMD_SERVO_DISABLE       = 0x0203,
    CMD_SERVO_GET_STATUS    = 0x0204,
    
    /* Sensor commands (0x03xx) */
    CMD_SENSOR_READ         = 0x0301,
    CMD_SENSOR_START_STREAM = 0x0302,
    CMD_SENSOR_STOP_STREAM  = 0x0303,
    
    /* System commands (0x05xx) */
    CMD_SYS_HEARTBEAT       = 0x0501,
    CMD_SYS_WATCHDOG        = 0x0502,
    CMD_SYS_EMERGENCY_STOP  = 0x0503,
    CMD_SYS_GET_STATE       = 0x0504,
    CMD_SYS_RESET           = 0x0505,
    
    /* ACK commands (0x06xx) */
    CMD_ACK_SUCCESS         = 0x0601,
    CMD_ACK_ERROR           = 0x0602,
} command_id_t;

/* ACK 状态码 */
typedef enum {
    ACK_SUCCESS             = 0,
    ACK_ERROR_PARAM         = 1,
    ACK_ERROR_TIMEOUT       = 2,
    ACK_ERROR_EXECUTION     = 3,
    ACK_ERROR_UNREGISTERED  = 4,
    ACK_ERROR_PERMISSION    = 5,
} ack_status_t;

/* 数据包结构 */
typedef struct __attribute__((packed)) {
    uint16_t head;              // 帧头 0xAA55
    uint8_t  version;           // 协议版本
    uint8_t  device_id;         // 设备 ID
    uint16_t command_id;        // 命令 ID
    uint16_t sequence_id;       // 序列号
    uint32_t timestamp;         // 时间戳
    uint16_t payload_length;    // 负载长度
    uint8_t  payload[MAX_PAYLOAD_SIZE];  // 负载数据
    uint16_t crc;               // CRC16 校验
} packet_t;

/* 函数声明 */
uint16_t crc16_calculate(const uint8_t *data, uint16_t length);
bool packet_verify_crc(const packet_t *packet);
void packet_build(packet_t *packet, uint8_t device_id, uint16_t command_id, 
                 const uint8_t *payload, uint16_t payload_len);
void packet_send(const packet_t *packet);
bool packet_receive(packet_t *packet);
void packet_handle(const packet_t *packet);

/* 电机控制 */
void motor_set_speed(uint8_t motor_id, float speed);
void motor_stop(uint8_t motor_id);

/* 系统功能 */
void system_heartbeat_response(void);
void system_emergency_stop(void);

#endif /* __ARF_PROTOCOL_H */
