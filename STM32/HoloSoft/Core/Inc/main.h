/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2019 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f7xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define SPI_4_CLK_Pin GPIO_PIN_2
#define SPI_4_CLK_GPIO_Port GPIOE
#define SPI_4_NCS_Pin GPIO_PIN_4
#define SPI_4_NCS_GPIO_Port GPIOE
#define SPI_4_MISO_Pin GPIO_PIN_5
#define SPI_4_MISO_GPIO_Port GPIOE
#define SPI_4_MOSI_Pin GPIO_PIN_6
#define SPI_4_MOSI_GPIO_Port GPIOE
#define SF_DM_2_Pin GPIO_PIN_7
#define SF_DM_2_GPIO_Port GPIOF
#define SLEW_DM_Pin GPIO_PIN_8
#define SLEW_DM_GPIO_Port GPIOF
#define INV_DM_Pin GPIO_PIN_9
#define INV_DM_GPIO_Port GPIOF
#define FB_DM_1_Pin GPIO_PIN_0
#define FB_DM_1_GPIO_Port GPIOC
#define FB_DM_2_Pin GPIO_PIN_1
#define FB_DM_2_GPIO_Port GPIOC
#define FB_DM_3_Pin GPIO_PIN_2
#define FB_DM_3_GPIO_Port GPIOC
#define FB_DM_4_Pin GPIO_PIN_3
#define FB_DM_4_GPIO_Port GPIOC
#define A_ENC_4_Pin GPIO_PIN_0
#define A_ENC_4_GPIO_Port GPIOA
#define B_ENC_4_Pin GPIO_PIN_1
#define B_ENC_4_GPIO_Port GPIOA
#define IN1_DM_2_Pin GPIO_PIN_2
#define IN1_DM_2_GPIO_Port GPIOA
#define IN2_DM_2_Pin GPIO_PIN_3
#define IN2_DM_2_GPIO_Port GPIOA
#define A_ENC_3_Pin GPIO_PIN_5
#define A_ENC_3_GPIO_Port GPIOA
#define IN1_DM_3_Pin GPIO_PIN_6
#define IN1_DM_3_GPIO_Port GPIOA
#define IN2_DM_3_Pin GPIO_PIN_7
#define IN2_DM_3_GPIO_Port GPIOA
#define ADC_VBATT_Pin GPIO_PIN_5
#define ADC_VBATT_GPIO_Port GPIOC
#define STM_GPIO1_Pin GPIO_PIN_1
#define STM_GPIO1_GPIO_Port GPIOB
#define STM_GPIO2_Pin GPIO_PIN_2
#define STM_GPIO2_GPIO_Port GPIOB
#define STM_GPIO3_Pin GPIO_PIN_11
#define STM_GPIO3_GPIO_Port GPIOF
#define STM_GPIO4_Pin GPIO_PIN_12
#define STM_GPIO4_GPIO_Port GPIOF
#define EEPROM_WC_Pin GPIO_PIN_13
#define EEPROM_WC_GPIO_Port GPIOF
#define ACC_SCL_Pin GPIO_PIN_14
#define ACC_SCL_GPIO_Port GPIOF
#define ACC_SDA_Pin GPIO_PIN_15
#define ACC_SDA_GPIO_Port GPIOF
#define EN_DM_1_Pin GPIO_PIN_9
#define EN_DM_1_GPIO_Port GPIOE
#define EN_DM_2_Pin GPIO_PIN_11
#define EN_DM_2_GPIO_Port GPIOE
#define EN_DM_3_Pin GPIO_PIN_13
#define EN_DM_3_GPIO_Port GPIOE
#define EN_DM_4_Pin GPIO_PIN_14
#define EN_DM_4_GPIO_Port GPIOE
#define SF_DM_3_Pin GPIO_PIN_15
#define SF_DM_3_GPIO_Port GPIOE
#define SPI_2_NCS_Pin GPIO_PIN_12
#define SPI_2_NCS_GPIO_Port GPIOB
#define SPI_2_CLK_Pin GPIO_PIN_13
#define SPI_2_CLK_GPIO_Port GPIOB
#define SPI_2_MISO_Pin GPIO_PIN_14
#define SPI_2_MISO_GPIO_Port GPIOB
#define SPI_2_MOSI_Pin GPIO_PIN_15
#define SPI_2_MOSI_GPIO_Port GPIOB
#define OUT_LE3_Pin GPIO_PIN_2
#define OUT_LE3_GPIO_Port GPIOG
#define OUT_LE4_Pin GPIO_PIN_3
#define OUT_LE4_GPIO_Port GPIOG
#define OUT_LE5_Pin GPIO_PIN_4
#define OUT_LE5_GPIO_Port GPIOG
#define OUT_LE6_Pin GPIO_PIN_5
#define OUT_LE6_GPIO_Port GPIOG
#define OUT_LE7_Pin GPIO_PIN_6
#define OUT_LE7_GPIO_Port GPIOG
#define CAPT_O_RST_Pin GPIO_PIN_7
#define CAPT_O_RST_GPIO_Port GPIOG
#define SPI_6_NCS_Pin GPIO_PIN_8
#define SPI_6_NCS_GPIO_Port GPIOG
#define A_ENC_2_Pin GPIO_PIN_6
#define A_ENC_2_GPIO_Port GPIOC
#define B_ENC_2_Pin GPIO_PIN_7
#define B_ENC_2_GPIO_Port GPIOC
#define IN1_DM_4_Pin GPIO_PIN_8
#define IN1_DM_4_GPIO_Port GPIOC
#define IN2_DM_4_Pin GPIO_PIN_9
#define IN2_DM_4_GPIO_Port GPIOC
#define ULTRA_DIR_Pin GPIO_PIN_8
#define ULTRA_DIR_GPIO_Port GPIOA
#define ULTRA_TX_Pin GPIO_PIN_9
#define ULTRA_TX_GPIO_Port GPIOA
#define ULTRA_RX_Pin GPIO_PIN_10
#define ULTRA_RX_GPIO_Port GPIOA
#define SF_DM_4_Pin GPIO_PIN_11
#define SF_DM_4_GPIO_Port GPIOA
#define WDI_Pin GPIO_PIN_12
#define WDI_GPIO_Port GPIOA
#define STM_SWSDIO_Pin GPIO_PIN_13
#define STM_SWSDIO_GPIO_Port GPIOA
#define STM_SWCLK_Pin GPIO_PIN_14
#define STM_SWCLK_GPIO_Port GPIOA
#define SPI_3_NCS_Pin GPIO_PIN_15
#define SPI_3_NCS_GPIO_Port GPIOA
#define SPI_3_CLK_Pin GPIO_PIN_10
#define SPI_3_CLK_GPIO_Port GPIOC
#define SPI_3_MISO_Pin GPIO_PIN_11
#define SPI_3_MISO_GPIO_Port GPIOC
#define SPI_3_MOSI_Pin GPIO_PIN_12
#define SPI_3_MOSI_GPIO_Port GPIOC
#define MOTION_3_Pin GPIO_PIN_0
#define MOTION_3_GPIO_Port GPIOD
#define MOTION_1_Pin GPIO_PIN_4
#define MOTION_1_GPIO_Port GPIOD
#define TTL_TX_Pin GPIO_PIN_5
#define TTL_TX_GPIO_Port GPIOD
#define TTL_RX_Pin GPIO_PIN_6
#define TTL_RX_GPIO_Port GPIOD
#define SPI_1_MOSI_Pin GPIO_PIN_7
#define SPI_1_MOSI_GPIO_Port GPIOD
#define SPI_1_MISO_Pin GPIO_PIN_9
#define SPI_1_MISO_GPIO_Port GPIOG
#define SPI_1_NCS_Pin GPIO_PIN_10
#define SPI_1_NCS_GPIO_Port GPIOG
#define SPI_1_CLK_Pin GPIO_PIN_11
#define SPI_1_CLK_GPIO_Port GPIOG
#define SPI_6_MISO_Pin GPIO_PIN_12
#define SPI_6_MISO_GPIO_Port GPIOG
#define SPI_6_CLK_Pin GPIO_PIN_13
#define SPI_6_CLK_GPIO_Port GPIOG
#define SPI_6_MOSI_Pin GPIO_PIN_14
#define SPI_6_MOSI_GPIO_Port GPIOG
#define MOTION_6_Pin GPIO_PIN_15
#define MOTION_6_GPIO_Port GPIOG
#define B_ENC_3_Pin GPIO_PIN_3
#define B_ENC_3_GPIO_Port GPIOB
#define SF_DM_1_Pin GPIO_PIN_5
#define SF_DM_1_GPIO_Port GPIOB
#define A_ENC_1_Pin GPIO_PIN_6
#define A_ENC_1_GPIO_Port GPIOB
#define B_ENC_1_Pin GPIO_PIN_7
#define B_ENC_1_GPIO_Port GPIOB
#define IN1_DM_1_Pin GPIO_PIN_8
#define IN1_DM_1_GPIO_Port GPIOB
#define IN2_DM_1_Pin GPIO_PIN_9
#define IN2_DM_1_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

#define MATHS_PI					3.14159

#define SAMPLING_TIME				0.02	// (seconde)
#define PID_TAU 					0.03

#define ENCODER_CPR					12

#define DUTYCYCLE_MAX				998
#define DUTYCYCLE_MIN				0

#define MOTOR_SPEED_MAX				8100
#define MOTOR_SPEED_MIN				-8100

#define ENCODER_SAMPLING_RATIO		((2 * MATHS_PI) / (4* ENCODER_CPR * SAMPLING_TIME))
#define RAD_TO_RPM					60 / (2*MATHS_PI)

#define DEBUG_print_com(msg)	HAL_UART_Transmit(&huart2, (uint8_t*)msg, sizeof(msg), HAL_MAX_DELAY)

#define DEBUG_print_var(msg, data)	uint8_t buff[50];\
									sprintf((char*)buff, msg, data);\
									HAL_UART_Transmit(&huart2, buff, strlen( (char*)buff ), 0xFFFF )

#define PID_ON					TRUE


// Variable de la plateforme
#define platformeWidth	307 		// Largeur de la plateforme - uinté: millimètre
#define platformeLength	400	// Longueur de la plateforme - uinté: millimètre
#define plateformeCenter	((platformeWidth / 2) - (wheelWidth / 2)) + ((platformeLength / 2) - (wheelDiameter / 2));	// Centre de la plateforme - uinté: millimètre
#define virtualPoint	plateformeCenter		// Reference de déplacement - uinté: millimètre

// Variable des blocs Moteur + encodeur + reducteur + roue
#define wheelWidth	50			// Largeur de la roue - uinté: millimètre
#define wheelDiameter	0.10		// Diamètre de la roue - uinté: mètre
#define wheelRadius		0.05 		// Rayon de la roue - uinté: mètre
#define position_Y_wheel	0.300 // en mètre
#define position_X_wheel	0.200 // en mètre
#define L1					0.13 // en mètre, cf: https://wiki.seeedstudio.com/4WD_Mecanum_Wheel_Robot_Kit_Series/
#define L2 					0.15 // en mètre, cf: https://wiki.seeedstudio.com/4WD_Mecanum_Wheel_Robot_Kit_Series/
#define wheelReducer	64		// Réduction entre le moteur et la roue
#define encodeurResolution		3070	// Nombre de front de l'encodeur pour un tour

#define motor_SpeedMaxP		848.23 // rad/s //= 8100.0 rpm
#define motor_SpeedMaxN		-motor_SpeedMaxP	// Vitesses de rotation maximum du moteur (P=positif, N=Négatif)
#define wheel_SpeedMaxP		50.0//13.25 // rad/s //= 126.5 rpm
#define wheel_SpeedMaxN		-wheel_SpeedMaxP	// Vitesses de rotation maximum de la roue (P=positif, N=Négatif)
#define pid_outputMaxP		wheel_SpeedMaxP
#define pid_outputMaxN		wheel_SpeedMaxN

#define PID_LIM_MIN 		-10.0f
#define PID_LIM_MAX 		10.0f

#define PID_LIM_MIN_INT 	-30.0f
#define PID_LIM_MAX_INT  	30.0f

#define pid_KP_WheelMotor1_rpm		2.0//2//0.05
#define pid_KP_WheelMotor2_rpm		2.0//2//0.05
#define pid_KP_WheelMotor3_rpm		2.0//2//0.05
#define pid_KP_WheelMotor4_rpm		2.0//2//0.05
#define pid_KI_WheelMotor1_rpm		25.0//0.05//0.5//0.5//5
#define pid_KI_WheelMotor2_rpm 		25.0//0.05//0.5//5
#define pid_KI_WheelMotor3_rpm 		25.0//0.05//0.5//5
#define pid_KI_WheelMotor4_rpm		25.0//0.05//0.5//5
#define pid_KD_WheelMotor1_rpm 		0.0//0.02//0.3//0
#define pid_KD_WheelMotor2_rpm 		0.0//0.02//0.3//0
#define pid_KD_WheelMotor3_rpm 		0.0//0.02//0.3//0
#define pid_KD_WheelMotor4_rpm		0.0//0.02//0.3//0


typedef enum{
	FALSE = 0,
	TRUE = 1
}bool_e;



// Variales Globale

 ADC_HandleTypeDef hadc1;
 ADC_HandleTypeDef hadc3;

 I2C_HandleTypeDef hi2c4;

 SPI_HandleTypeDef hspi1;
 SPI_HandleTypeDef hspi2;
 SPI_HandleTypeDef hspi3;
 SPI_HandleTypeDef hspi4;
 SPI_HandleTypeDef hspi6;

 TIM_HandleTypeDef htim2;
 TIM_HandleTypeDef htim3;
 TIM_HandleTypeDef htim4;
 TIM_HandleTypeDef htim5;
 TIM_HandleTypeDef htim6;
 TIM_HandleTypeDef htim7;
 TIM_HandleTypeDef htim8;
 TIM_HandleTypeDef htim9;
 TIM_HandleTypeDef htim10;
 TIM_HandleTypeDef htim11;
 TIM_HandleTypeDef htim13;
 TIM_HandleTypeDef htim14;

 UART_HandleTypeDef huart1;
 UART_HandleTypeDef huart2;
 UART_HandleTypeDef huart3;


/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
