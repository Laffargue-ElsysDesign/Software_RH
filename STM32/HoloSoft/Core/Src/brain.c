/*
 * brain.c
 *
 *  Created on: 11 juin 2020
 *      Author: Guillaume
 */

#include "main.h"
#include "brain.h"
#include "debug.h"
#include "secretary.h"

uint8_t statusflag_Motor1, statusflag_Motor2, statusflag_Motor3, statusflag_Motor4;
HAL_UART_StateTypeDef state = 0;
void BRAIN_main(){
	SECRETARY_send_to_UltraBrain(RESTART, 0);
	while (TRUE)
	{

		//SECRETARY_process_main();
	//	DEBUG_print_odometry();
	//	SECRETARY_send_to_UltraBrain(ODOMETRY);
	//	DEBUG_print_cmd();
	//	DEBUG_print_com("coucou");
	//	HAL_UART_Transmit(&huart2, (uint8_t*)"***********************************\r\n", sizeof("***********************************\r\n"), HAL_MAX_DELAY);
	//	HAL_UART_Transmit(&huart2, (uint8_t*)"* AsserVitesse_V01                *\r\n", sizeof("* AsserVitesse_V01                *\r\n"), HAL_MAX_DELAY);

		//	  if (HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13)) {	                // checks if PA0 is set
		//		  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);      // switch on LED6
		//	  } else {
		//		  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);    // switch off LED6
		//	  }
		/*if(angle_deg > 360-1) {
			  angle_deg = 0;
		  }*/

		// MOVE - commande par vecteur et angle - Déplacement en X/Y
		//target_WheelMotor1_rpm = -vecteur * cos((M_PI / 180) * angle_deg + (M_PI / 4)); // Cette commande est OK
		//target_WheelMotor2_rpm = -vecteur * sin((M_PI / 180) * angle_deg + (M_PI / 4));	// Vecteur + angle
		//target_WheelMotor3_rpm =  vecteur * cos((M_PI / 180) * angle_deg + (M_PI / 4));
		//target_WheelMotor4_rpm =  vecteur * sin((M_PI / 180) * angle_deg + (M_PI / 4));



		// MOVE - commande par vecteur et angle - Déplacement en X/Y + possibilité de rotation en Wz
		/*target_WheelMotor1_rpm = -(cmd_x - cmd_y - (virtualPoint*cmd_z));
		  target_WheelMotor2_rpm = (cmd_x + cmd_y - (virtualPoint*cmd_z));
		  target_WheelMotor3_rpm = (cmd_x - cmd_y + (virtualPoint*cmd_z));
		  target_WheelMotor4_rpm = -(cmd_x + cmd_y + (virtualPoint*cmd_z));*/

		//target_WheelMotor1_rpm = -(cmd_x + cmd_y - cmd_z);
		//target_WheelMotor2_rpm =  (cmd_x - cmd_y + cmd_z);
		//target_WheelMotor3_rpm =  (cmd_x + cmd_y + cmd_z);
		//target_WheelMotor4_rpm = -(cmd_x - cmd_y - cmd_z);



	//	HAL_Delay(50);
		/* Vérification du STATUS_FLAG des moteurs */
		statusflag_Motor1 = HAL_GPIO_ReadPin(SF_DM_1_GPIO_Port, SF_DM_1_Pin);
		statusflag_Motor2 = HAL_GPIO_ReadPin(SF_DM_2_GPIO_Port, SF_DM_2_Pin);
		statusflag_Motor3 = HAL_GPIO_ReadPin(SF_DM_3_GPIO_Port, SF_DM_3_Pin);
		statusflag_Motor4 = HAL_GPIO_ReadPin(SF_DM_4_GPIO_Port, SF_DM_4_Pin);
		if(statusflag_Motor1 | statusflag_Motor2 | statusflag_Motor3 | statusflag_Motor4) {
			HAL_GPIO_WritePin(EN_DM_1_GPIO_Port, EN_DM_1_Pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(EN_DM_2_GPIO_Port, EN_DM_2_Pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(EN_DM_3_GPIO_Port, EN_DM_3_Pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(EN_DM_4_GPIO_Port, EN_DM_4_Pin, GPIO_PIN_SET);
			HAL_GPIO_WritePin(OUT_LE7_GPIO_Port, OUT_LE7_Pin, GPIO_PIN_RESET);
		}
		else {
			HAL_GPIO_WritePin(EN_DM_1_GPIO_Port, EN_DM_1_Pin, GPIO_PIN_RESET);
			HAL_GPIO_WritePin(EN_DM_2_GPIO_Port, EN_DM_2_Pin, GPIO_PIN_RESET);
			HAL_GPIO_WritePin(EN_DM_3_GPIO_Port, EN_DM_3_Pin, GPIO_PIN_RESET);
			HAL_GPIO_WritePin(EN_DM_4_GPIO_Port, EN_DM_4_Pin, GPIO_PIN_RESET);
			HAL_GPIO_WritePin(OUT_LE7_GPIO_Port, OUT_LE7_Pin, GPIO_PIN_SET);
		}



		//target_WheelMotor1_rpm = -(CMD_EXT.x + CMD_EXT.y - CMD_EXT.w);
		//target_WheelMotor2_rpm =  (CMD_EXT.x - CMD_EXT.y + CMD_EXT.w);
		//target_WheelMotor3_rpm =  (CMD_EXT.x + CMD_EXT.y + CMD_EXT.w);
		//target_WheelMotor4_rpm = -(CMD_EXT.x - CMD_EXT.y - CMD_EXT.w);




		//if(debug > 50000) {
		//sprintf(buffer, "CMD: %d %d %d\r\n", cmd_rpm[0], cmd_rpm[1], cmd_rpm[2]);
		//sprintf(buffer, "CMD: %d %d %d %d\r\n", target_velocity_rpm_m1, target_velocity_rpm_m2, target_velocity_rpm_m3, target_velocity_rpm_m4);
		//sprintf(buffer, "CMD: %d %d %d %d\r\n", current_velocity_rpm_m1, current_velocity_rpm_m2, current_velocity_rpm_m3, current_velocity_rpm_m4);
		//sprintf(buffer, "CMD: %d %d %d\r\n", MOTOR1.current_speed, MOTOR1.current_encodeur, MOTOR1.duty_cycle);
		//sprintf(buffer, "CMD: %d %d %d\r\n", CMD_JOYSTICK.x, CMD_JOYSTICK.y, CMD_JOYSTICK.w);
		//sprintf(buffer, "CMD: %d %d %d %d\r\n", PID_M1.target, PID_M1.output, PID_M1.last_error, PID_M1.current_error);

		//sprintf(buffer, "CMD: %d %d %d %d\r\n", current_error_position_m1, current_error_position_m2, current_error_position_m3, current_error_position_m4);
		//sprintf(buffer, "CMD: %d %d %d %d\r\n", pwm_m1, pwm_m2, pwm_m3, pwm_m4);

		//sprintf(buffer, "CMD: %d %d %d %d\r\n", current_position_m1, current_position_m2, current_position_m3, current_position_m4);
		//sprintf(buffer, "SPI: %02X %02X %02X %02X %02X\r\n", spi2_rx[0], spi2_rx[1], spi2_rx[2], spi2_rx[3], spi2_rx[4]);

		//sprintf(buffer, ">> %d : %d : %d : %d : %d : %d : 0x%04X\r\n", joystick_p_left_y, joystick_p_left_x, joystick_p_lt, joystick_p_right_x, joystick_p_right_y, joystick_p_rt, joystick_buttons );
		//sprintf(buffer, ">> 0x%02X,0x%02X | 0x%02X,0x%02X | 0x%02X,0x%02X | 0x%02X,0x%02X | 0x%02X,0x%02X | 0x%02X,0x%02X | 0x%02X,0x%02X\r\n", spi4_rx[0], spi4_rx[1], spi4_rx[2], spi4_rx[3], spi4_rx[4], spi4_rx[5], spi4_rx[6], spi4_rx[7], spi4_rx[8], spi4_rx[9], spi4_rx[10], spi4_rx[11], spi4_rx[12], spi4_rx[13]);
		//sprintf(buffer, "CMD: %d %d %d\r\n", CMD_EXT.x, CMD_EXT.y, CMD_EXT.w);
		//sprintf(buffer, "CMD: %d %d %d\r\n", cmd_regiter, external_x, external_y);

		//sprintf(buffer, "DIR: %d\r\n", __HAL_TIM_IS_TIM_COUNTING_DOWN(&htim4));
		//sprintf(buffer, "Vel: %d\r\n", (int16_t)current_velocity_rpm_m1);

		//sprintf(buffer, "x:%d y:%d w:%d * v1:%d v2:%d v3:%d v4:%d\r\n", x, y, w, v1, v2, v3, v4);
		//sprintf(buffer, "angle:%d* v1:%d v2:%d v3:%d v4:%d \r\n", angle_deg, (int16_t)speed_WheelMotor1_rpm, (int16_t)speed_WheelMotor2_rpm, (int16_t)speed_WheelMotor3_rpm, (int16_t)speed_WheelMotor4_rpm);
		//	  	  sprintf(buffer, "v1:%d v2:%d v3:%d v4:%d \r\n", (int16_t)speed_WheelMotor1_rpm, (int16_t)speed_WheelMotor2_rpm, (int16_t)speed_WheelMotor3_rpm, (int16_t)speed_WheelMotor4_rpm);
		//sprintf(buffer, "OUT: %d\r\n", output_m1);
		//sprintf(buffer, "PID: %d - Targ: %d - Speed: %d - pidOut: %d - Pwm: %d\r\n", PID_ON, (int16_t)target_WheelMotor1_rpm, (int16_t)speed_WheelMotor1_rpm, (int16_t)pid_output_WheelMotor1_rpm, (int16_t)dutycycle_Motor1);
		//sprintf(buffer, "PWM: %d\r\n", dutycycle_Motor1);
		//sprintf(buffer, "PID_out: %d\r\n", pid_output_WheelMotor1_rpm);
		//sprintf(buffer, "In1: %d * In2: %d * Pwm: %d\r\n", HAL_GPIO_ReadPin(IN1_DM_1_GPIO_Port, IN1_DM_1_Pin), HAL_GPIO_ReadPin(IN2_DM_1_GPIO_Port, IN2_DM_1_Pin), MOTORWHEEL_FL.dutyCycle);
		//sprintf(buffer, "OUT: %d\r\n", acceleration);
		//		  HAL_UART_Transmit(&huart2,(uint8_t *)buffer, sizeof(buffer), HAL_MAX_DELAY);


		//sprintf(buffer, "SPI_Rx: %02x %02x %02x\r\n", rx_spi[0] ,rx_spi[1], rx_spi[2]);
		//sprintf(buffer, "SPI_Rx: %d %d %d %d\r\n", cmd_rpm[0], cmd_rpm[1], cmd_rpm[2]);
		//HAL_UART_Transmit(&huart2,(uint8_t *)buffer, sizeof(buffer), HAL_MAX_DELAY);
		//sprintf(buffer, "STM_Rx: 0x%02X 0x%02X 0x%02X 0x%02X\r\n", spi4_buffer[0], spi4_buffer[1], spi4_buffer[2], spi4_buffer[3]);
		//debug = 0;
		//}

		//debug++;

		//angle_deg += 5;

		//  HAL_Delay(50);

		/* USER CODE END WHILE */

		/* USER CODE BEGIN 3 */
	}
}
