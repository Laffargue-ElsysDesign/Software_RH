/*
 * it.c
 *
 *  Created on: Jun 11, 2020
 *      Author: Guillaume
 */


#include "main.h"
#include "it.h"
#include "pilote.h"
#include "joystick.h"
#include "secretary.h"


uint8_t	spi4_rx[14] = {0};
uint8_t data_uart[16] = {0};
uint16_t it_trace = 0;
void IT_init(){
	HAL_TIM_Base_Start_IT(&htim7);
	HAL_TIM_Base_Start_IT(&htim6);

//	HAL_SPI_Receive_IT(&hspi4, spi4_rx, sizeof(spi4_rx));
	HAL_UART_Receive_IT(&huart3, data_uart, sizeof(data_uart));
}

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {
	if(htim->Instance == TIM7) {//20ms
		PILOTE_mouv();
	}
	if(htim->Instance == TIM6) {//1000ms
		PILOTE_stop();
	}
}

void HAL_SPI_RxCpltCallback(SPI_HandleTypeDef *hspi) {
	if(hspi->Instance == SPI4) {
		JOYSTICK_recieve_order(spi4_rx);
	}
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){
	if(huart->Instance == USART3) {
		SECRETARY_dispatcher(data_uart);
		//HAL_GPIO_TogglePin(OUT_LE3_GPIO_Port, OUT_LE3_Pin);
		//HAL_UART_Abort_IT(&huart3);
		//HAL_UART_Transmit(&huart3, data_uart, sizeof(data_uart),100);
		SECRETARY_process_main();
		HAL_UART_Receive_IT(&huart3, data_uart, sizeof(data_uart));

	}


}
