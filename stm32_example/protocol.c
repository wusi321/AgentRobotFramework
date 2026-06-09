/**
 * ARF STM32 Protocol Implementation
 * STM32 协议实现示例
 */

#include "protocol.h"
#include <string.h>

/* CRC16 计算 */
uint16_t crc16_calculate(const uint8_t *data, uint16_t length) {
    uint16_t crc = 0xFFFF;
    uint16_t polynomial = 0xA001;
    
    for (uint16_t i = 0; i < length; i++) {
        crc ^= data[i];
        for (uint8_t j = 0; j < 8; j++) {
            if (crc & 0x0001) {
                crc = (crc >> 1) ^ polynomial;
            } else {
                crc >>= 1;
            }
        }
    }
    
    return crc;
}

/* 验证 CRC */
bool packet_verify_crc(const packet_t *packet) {
    uint16_t data_length = 15 + packet->payload_length;
    uint16_t calculated_crc = crc16_calculate((const uint8_t*)packet, data_length);
    return calculated_crc == packet->crc;
}

/* 构建数据包 */
void packet_build(packet_t *packet, uint8_t device_id, uint16_t command_id, 
                 const uint8_t *payload, uint16_t payload_len) {
    packet->head = FRAME_HEAD;
    packet->version = PROTOCOL_VERSION;
    packet->device_id = device_id;
    packet->command_id = command_id;
    packet->sequence_id = 0;  // 由上层管理
    packet->timestamp = 0;     // 使用系统时钟
    packet->payload_length = payload_len;
    
    if (payload && payload_len > 0) {
        memcpy(packet->payload, payload, payload_len);
    }
    
    // 计算 CRC
    uint16_t data_length = 15 + payload_len;
    packet->crc = crc16_calculate((const uint8_t*)packet, data_length);
}

/* 发送数据包 */
void packet_send(const packet_t *packet) {
    uint16_t total_length = 15 + packet->payload_length + 2;
    
    // 使用 UART 发送
    // HAL_UART_Transmit(&huart1, (uint8_t*)packet, total_length, 1000);
}

/* 处理数据包 */
void packet_handle(const packet_t *packet) {
    // 验证 CRC
    if (!packet_verify_crc(packet)) {
        return;
    }
    
    // 根据命令 ID 分发处理
    switch (packet->command_id) {
        case CMD_MOTOR_SET_SPEED: {
            uint8_t motor_id = packet->payload[0];
            float speed;
            memcpy(&speed, &packet->payload[1], sizeof(float));
            motor_set_speed(motor_id, speed);
            break;
        }
        
        case CMD_MOTOR_STOP: {
            uint8_t motor_id = packet->payload[0];
            motor_stop(motor_id);
            break;
        }
        
        case CMD_SYS_HEARTBEAT:
            system_heartbeat_response();
            break;
        
        case CMD_SYS_EMERGENCY_STOP:
            system_emergency_stop();
            break;
        
        default:
            // 未知命令
            break;
    }
}

/* 电机控制实现示例 */
void motor_set_speed(uint8_t motor_id, float speed) {
    // 实现电机控制
    // 例如：设置 PWM 占空比
    
    // 发送 ACK
    packet_t ack;
    uint8_t ack_payload[1] = {ACK_SUCCESS};
    packet_build(&ack, 1, CMD_ACK_SUCCESS, ack_payload, 1);
    packet_send(&ack);
}

void motor_stop(uint8_t motor_id) {
    // 停止电机
    // 例如：PWM 占空比设为 0
    
    // 发送 ACK
    packet_t ack;
    uint8_t ack_payload[1] = {ACK_SUCCESS};
    packet_build(&ack, 1, CMD_ACK_SUCCESS, ack_payload, 1);
    packet_send(&ack);
}

/* 系统功能 */
void system_heartbeat_response(void) {
    packet_t response;
    packet_build(&response, 0, CMD_ACK_SUCCESS, NULL, 0);
    packet_send(&response);
}

void system_emergency_stop(void) {
    // 紧急停止所有电机
    // 最高优先级，立即执行
    
    // 停止所有 PWM 输出
    // 进入安全模式
}
