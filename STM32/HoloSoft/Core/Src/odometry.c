/*
 * odometry.c
 *
 *  Created on: Jun 11, 2020
 *      Author: Guillaume
 */
#include <stdlib.h>
#include "main.h"
#include "odometry.h"
#include "pilote.h"
#include "math.h"
#include "debug.h"



static int64_t encodeurTour = 0;
static int16_t encoder_Motor1, encoder_Motor2, encoder_Motor3, encoder_Motor4;
static int16_t last_encoder1 = 0;
static int16_t last_encoder2 = 0;
static int16_t last_encoder3, last_encoder4;
static bool_e is_init = FALSE;
static int16_t i;
static ODOMETRY_speed_wheel wheels_speed;
static ODOMETRY_speed_robot robot_speed;


static double X, Y, Z;
int16_t time2, old_time, freq;

void ODOMETRY_init(){
	last_encoder1 = 0;
	last_encoder2 = 0;
	last_encoder3 = 0;
	last_encoder4 = 0;
}


void ODOMETRY_it_5ms(){

}


ODOMETRY_speed_wheel ODOMETRY_it_10ms(){

	/*double pietEncode1,pietEncode2,pietEncode3, pietEncode4;
	double SR = 0;*/
	HAL_GPIO_TogglePin(STM_GPIO1_GPIO_Port, STM_GPIO1_Pin);
	encoder_Motor1 = ((double)__HAL_TIM_GET_COUNTER(&htim4)); //perte de quelque impulsion
	encoder_Motor2 = ((double)__HAL_TIM_GET_COUNTER(&htim3));
	encoder_Motor3 = ((double)__HAL_TIM_GET_COUNTER(&htim2));
	encoder_Motor4 = ((double)__HAL_TIM_GET_COUNTER(&htim5));

	__HAL_TIM_SET_COUNTER(&htim4, 0);
	__HAL_TIM_SET_COUNTER(&htim3, 0);
	__HAL_TIM_SET_COUNTER(&htim2, 0);
	__HAL_TIM_SET_COUNTER(&htim5, 0);

	/*pietEncode1 = (2*(double)(M_PI)*(-encoder_Motor1));
	pietEncode2 = (2*(double)(M_PI)*(-encoder_Motor2));
	pietEncode3 = (2*(double)(M_PI)*(encoder_Motor3));
	pietEncode4 = (2*(double)(M_PI)*(encoder_Motor4));

	SR =(encodeurResolution/SAMPLING_TIME);*/
	/*wheels_speed.speed_WheelMotor1_rpm = (2*(double)(M_PI)*(double)SAMPLING_TIME*(-encoder_Motor1))/(double)encodeurResolution;  // rad/s
	wheels_speed.speed_WheelMotor2_rpm = (2*(double)(M_PI)*(double)SAMPLING_TIME*(-encoder_Motor2))/(double)encodeurResolution;
	wheels_speed.speed_WheelMotor3_rpm = (2*(double)(M_PI)*(double)SAMPLING_TIME*(encoder_Motor3))/(double)encodeurResolution;
	wheels_speed.speed_WheelMotor4_rpm = (2*(double)(M_PI)*(double)SAMPLING_TIME*(encoder_Motor4))/(double)encodeurResolution;*/

	wheels_speed.speed_WheelMotor1_rpm = (-encoder_Motor1)/((double)encodeurResolution*(double)SAMPLING_TIME);  // rad/s
	wheels_speed.speed_WheelMotor2_rpm = (-encoder_Motor2)/((double)encodeurResolution*(double)SAMPLING_TIME); //tr/s
	wheels_speed.speed_WheelMotor3_rpm = (encoder_Motor3)/((double)encodeurResolution*(double)SAMPLING_TIME);
	wheels_speed.speed_WheelMotor4_rpm = (encoder_Motor4)/((double)encodeurResolution*(double)SAMPLING_TIME);

	//	DEBUG_update_corrector(0,0,0,0,encoder_Motor1,encoder_Motor2,encoder_Motor3,encoder_Motor4, last_encoder1,last_encoder2, last_encoder3, last_encoder4);

	ODOMETRY_calcul_speed_robot(wheels_speed);

	return wheels_speed;
}

ODOMETRY_speed_wheel ODOMETRY_get_speed_wheels(){
	return wheels_speed;
}

ODOMETRY_speed_robot ODOMETRY_get_speed_robot(){
	return robot_speed;
}

void ODOMETRY_calcul_speed_robot(ODOMETRY_speed_wheel wheels_speed){

	robot_speed.speed_X    = ( wheels_speed.speed_WheelMotor4_rpm + wheels_speed.speed_WheelMotor1_rpm + wheels_speed.speed_WheelMotor2_rpm + wheels_speed.speed_WheelMotor3_rpm) * (wheelDiameter*M_PI/4); //en mètre/s
	robot_speed.speed_Y    = (-wheels_speed.speed_WheelMotor4_rpm + wheels_speed.speed_WheelMotor1_rpm - wheels_speed.speed_WheelMotor2_rpm + wheels_speed.speed_WheelMotor3_rpm) * (wheelDiameter*M_PI/4); //en mètre/s
	robot_speed.speed_teta = ( wheels_speed.speed_WheelMotor4_rpm - wheels_speed.speed_WheelMotor1_rpm - wheels_speed.speed_WheelMotor2_rpm + wheels_speed.speed_WheelMotor3_rpm) * (wheelDiameter*M_PI/(4*(L1+L2))); // rad/s

	robot_speed.dist_X = robot_speed.dist_X + ( (-encoder_Motor1 - encoder_Motor2 + encoder_Motor3 + encoder_Motor4 )/(4*(double)encodeurResolution))*((double)(M_PI)*wheelDiameter); //en mètre/s
	robot_speed.dist_Y = robot_speed.dist_Y + ( (-encoder_Motor1 + encoder_Motor2 + encoder_Motor3 - encoder_Motor4 )/(4*(double)encodeurResolution))*((double)(M_PI)*wheelDiameter); //en mètre/s
	robot_speed.teta_Z = robot_speed.teta_Z + ( (encoder_Motor1 + encoder_Motor2 + encoder_Motor3 + encoder_Motor4 )/(4*(double)encodeurResolution))*((double)(M_PI)*wheelDiameter/((L1+L2)))*57,2957795; //en mètre/s

	//	DEBUG_update_odometry(robot_speed.speed_X, robot_speed.speed_Y, robot_speed.speed_teta,wheels_speed.speed_WheelMotor1_rpm , wheels_speed.speed_WheelMotor2_rpm , wheels_speed.speed_WheelMotor3_rpm , wheels_speed.speed_WheelMotor4_rpm, 0, 0, 0);

	/*X += robot_speed.speed_X*0.01;
	Y += robot_speed.speed_Y*0.01;
	Z += robot_speed.speed_teta*0.01;*/
}
