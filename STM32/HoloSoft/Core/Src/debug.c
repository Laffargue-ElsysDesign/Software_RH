/*
 * debug.c
 *
 *  Created on: 15 juin 2020
 *      Author: Guillaume
 */

#include <stdio.h>
#include <string.h>
#include "main.h"
#include "debug.h"
static uint32_t start_time = 0;
static double debug_odometry[10] = {0};
static bool_e is_print_yet_odom = FALSE;

static double debug_corrector[13] = {0};
static bool_e is_print_yet_corrector = FALSE;

static double debug_cmd[5] = {0};
static bool_e is_print_yet_cmd = FALSE;


void DEBUG_update_odometry(double speedXr, double speedYr, double speedTeta, double speedXw, double speedYw, double teta, double Xr, double Yr, double Xw, double Yw){
	start_time++;
	debug_odometry[0] = speedXr;
	debug_odometry[1] = speedYr;
	debug_odometry[2] = speedTeta;
	debug_odometry[3] = speedXw;
	debug_odometry[4] = speedYw;
	debug_odometry[5] = teta;
	debug_odometry[6] = Xr;
	debug_odometry[7] = Yr;
	debug_odometry[8] = Xw;
	debug_odometry[9] = Yw;
	is_print_yet_odom = FALSE;

}

void DEBUG_print_odometry(){

	uint8_t buff[50] = {0};
	if(!is_print_yet_odom){
		sprintf((char*)buff, "%d", (int)start_time);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_odometry[0]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_odometry[1]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_odometry[2]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_odometry[3]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_odometry[4]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_odometry[5]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_odometry[6]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_odometry[7]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_odometry[8]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%d", (int)debug_odometry[9]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		DEBUG_print_com("\n");
		is_print_yet_odom = TRUE;
	}

}


void DEBUG_update_corrector(double target_WheelMotor1_rpm, double target_WheelMotor2_rpm, double target_WheelMotor3_rpm, double target_WheelMotor4_rpm, double pid_error_WheelMotor1_rpm, double pid_error_WheelMotor2_rpm, double pid_error_WheelMotor3_rpm, double pid_error_WheelMotor4_rpm, double speed_WheelMotor1_rpm, double speed_WheelMotor2_rpm, double speed_WheelMotor3_rpm, double speed_WheelMotor4_rpm){
	start_time++;
	debug_corrector[0] = target_WheelMotor1_rpm;
	debug_corrector[1] = target_WheelMotor2_rpm;
	debug_corrector[2] = target_WheelMotor3_rpm;
	debug_corrector[3] = target_WheelMotor4_rpm;
	debug_corrector[4] = pid_error_WheelMotor1_rpm;
	debug_corrector[5] = pid_error_WheelMotor2_rpm;
	debug_corrector[6] = pid_error_WheelMotor3_rpm;
	debug_corrector[7] = pid_error_WheelMotor4_rpm;
	debug_corrector[8] = speed_WheelMotor1_rpm;
	debug_corrector[9] = speed_WheelMotor2_rpm;
	debug_corrector[10] = speed_WheelMotor3_rpm;
	debug_corrector[11] = speed_WheelMotor4_rpm;
	is_print_yet_corrector = FALSE;

}


void DEBUG_print_corrector(){

	uint8_t buff[50];
	if(!is_print_yet_corrector){
		sprintf((char*)buff, "%d", (int)start_time);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_corrector[0]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_corrector[1]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_corrector[2]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_corrector[3]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_corrector[4]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_corrector[5]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_corrector[6]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_corrector[7]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", (debug_corrector[8]));
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", (debug_corrector[9]));
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", (debug_corrector[10]));
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", (debug_corrector[11]));
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		DEBUG_print_com("\n");
		is_print_yet_corrector = TRUE;
	}

}




void DEBUG_update_cmd(int16_t x, int16_t y, int16_t z){
	start_time++;
	debug_cmd[0] = x;
	debug_cmd[1] = y;
	debug_cmd[2] = z;


	is_print_yet_cmd = FALSE;

}


void DEBUG_print_cmd(){

	uint8_t buff[50];
	if(!is_print_yet_cmd){
		sprintf((char*)buff, "%d", (int)start_time);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%d", (int)debug_cmd[0]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%d", (int)debug_cmd[1]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );

		sprintf((char*)buff, ";%f", debug_cmd[2]);
		HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF );





		DEBUG_print_com("\n");
		is_print_yet_cmd = TRUE;
	}

}








