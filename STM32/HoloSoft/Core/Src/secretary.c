/*
 * secretary.c
 *
 *  Created on: Jun 10, 2020
 *      Author: Guillaume
 */


#include "main.h"
#include "stm32f7xx_hal_uart.h"
#include "secretary.h"
#include "pilote.h"
#include "odometry.h"
#include "debug.h"
#define PROTOCOL_LENGHT 15
#define MSG_LENGHT 16

uint64_t holo_CNT = 0;

static bool_e is_msg_to_send = FALSE;
static int8_t msg_to_send[MSG_LENGHT] = {0};
static bool_e message_not_long = FALSE;
static uint16_t msg_len = 0;

static double test_x = -1.186789123;


void SECRETARY_dispatcher(uint8_t* data){
	bool_e cmd_read = FALSE;
	SECRETARY_protocol protocol_state = SOF;
	bool_e error_msg = FALSE;
	bool_e msg_ok = FALSE;
	do{
		switch (protocol_state){
		case SOF:
			if(data[SOF] != 0x5A){
				HAL_GPIO_TogglePin(OUT_LE4_GPIO_Port, OUT_LE4_Pin);
				error_msg = TRUE;
			}else{
				HAL_GPIO_TogglePin(OUT_LE5_GPIO_Port, OUT_LE5_Pin);
				protocol_state = EndOfFrame;
			}
			break;
		case CMD:
			/*if (data[CMD] & 1 << ODOMETRY){
				SECRETARY_send_to_UltraBrain(ODOMETRY, data[CNT]);
				cmd_read = TRUE;
			}
			if(data[CMD] & (1 << MOUVEMENT)){*/
				//HAL_GPIO_TogglePin(OUT_LE6_GPIO_Port, OUT_LE6_Pin);
				PILOTE_recieve_cmd(((double)(int32_t)data[BYTE0]), ((double)(int32_t)data[BYTE1]), ((double)(int32_t)data[BYTE2]));
				SECRETARY_send_to_UltraBrain(ODOMETRY, 40);
				msg_ok = TRUE;
				cmd_read = TRUE;
			/*}
			if(data[CMD] & (1 << RESTART)){
				HAL_NVIC_SystemReset();
				cmd_read = TRUE;
			}
			if(data[CMD] & (1 << VOLTAGE)){
				//	BATTERY_ask_voltage();
				cmd_read = TRUE;
			}
			if(!cmd_read){
				error_msg = FALSE;
			}else{
				msg_ok = TRUE;
			}*/
			break;
		case STATUS:
			protocol_state = CMD;
			break;
		case CNT:
			if(TRUE){//data[CNT] == holo_CNT){
				protocol_state = STATUS;
			}else{
				error_msg = TRUE;
			}
			break;
		case NBYTES:
			break;
		case CHK:
			protocol_state = CNT;
			break;
		case EndOfFrame:
			if(data[EndOfFrame] != 0xA5){
				error_msg = TRUE;
			}else{
				protocol_state = CMD;//CHK;
			}
			break;
		default:
			error_msg = TRUE;
			break;
		}
	}while ( !msg_ok && !error_msg);

	if(error_msg == TRUE){
		HAL_NVIC_SystemReset();
	}
}


void SECRETARY_send_to_UltraBrain(SECRETARY_cmd_ultra cmd, uint8_t CouNT){
	uint8_t status = 0;

	msg_to_send[SOF]    	=   0x5A;
	msg_to_send[CMD]    	=   1<<cmd;
	msg_to_send[STATUS] 	=	status;
	msg_to_send[CNT]    	=	holo_CNT;
	msg_to_send[NBYTES] 	=	0;
	msg_to_send[BYTE0]  	=	0;
	msg_to_send[BYTE1] 		=	0;
	msg_to_send[BYTE2] 		=	0;
	msg_to_send[BYTE3]  	=	0;
	msg_to_send[BYTE4]  	=	0;
	msg_to_send[BYTE5]  	=	0;
	msg_to_send[BYTE6]  	=	0;
	msg_to_send[BYTE7]  	=	0;
	msg_to_send[BYTE8]  	=	0;
	msg_to_send[CHK]    	=	0;
	msg_to_send[EndOfFrame] =	0xA5;

	ODOMETRY_speed_robot speed_robot = ODOMETRY_get_speed_robot();
	switch(cmd){
	case ODOMETRY:{


		/*msg_to_send[BYTE0] = (int8_t)(speed_robot.speed_X);//(((int16_t)(speed_robot.speed_X*32000)) >> 8);
		msg_to_send[BYTE1] = (int8_t)((int16_t)speed_robot.speed_X >> 8);



		msg_to_send[BYTE2] = (int8_t)(((int16_t)(speed_robot.speed_Y*32000)) >> 8);
		msg_to_send[BYTE3] = (int8_t)((((int16_t)(speed_robot.speed_Y*32000)) << 8) >> 8);


		msg_to_send[BYTE4] = (int8_t)(((int16_t)(speed_robot.speed_teta*32000)) >> 8);
		msg_to_send[BYTE5] = (int8_t)((((int16_t)(speed_robot.speed_teta*32000)) << 8) >> 8);*/

		msg_to_send[BYTE0] = (int8_t)(speed_robot.speed_X*1000);//(((int16_t)(speed_robot.speed_X*32000)) >> 8);
		msg_to_send[BYTE1] = (int8_t)(speed_robot.speed_X*100);



		msg_to_send[BYTE2] = (int8_t)(test_x*100);
		msg_to_send[BYTE3] = (int8_t)(speed_robot.speed_Y*100);


		msg_to_send[BYTE4] = (int8_t)(test_x*100);
		msg_to_send[BYTE5] = (int8_t)(speed_robot.speed_teta*100);


		msg_to_send[BYTE6] = (int8_t)(speed_robot.dist_X*100);
		msg_to_send[BYTE7] = (int8_t)(speed_robot.dist_Y*100);
		msg_to_send[BYTE8] = (int8_t)(-speed_robot.teta_Z);

		speed_robot.dist_X = 0;
		speed_robot.dist_Y = 0;
		speed_robot.teta_Z = 0;

		break;}
	case RESTART:

		break;
	default:
		break;
	}

	//DEBUG_update_odometry(msg_to_send[BYTE0],msg_to_send[BYTE1],msg_to_send[BYTE2],msg_to_send[BYTE3],msg_to_send[BYTE4],msg_to_send[BYTE5],speed_robot.speed_X, speed_robot.speed_Y, speed_robot.speed_teta,0);


	is_msg_to_send = TRUE;
	/*msg_len = sizeof(msg_to_send);
	if(msg_len < 16){
		message_not_long = TRUE;
	}
	HAL_UART_Transmit(&huart3, (uint8_t*)msg_to_send, MSG_LENGHT, HAL_MAX_DELAY);*/
	//SECRETARY_process_main();
	holo_CNT++;


}


void SECRETARY_process_main(){
	if(is_msg_to_send){
		is_msg_to_send = FALSE;
		msg_len = sizeof(msg_to_send);
		if(msg_len < 16){
			message_not_long = TRUE;
		}
		HAL_UART_Transmit(&huart3, (uint8_t*)msg_to_send, MSG_LENGHT, HAL_MAX_DELAY);

	}
}
