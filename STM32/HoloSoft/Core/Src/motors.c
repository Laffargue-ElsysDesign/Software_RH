/*
 * motors.c
 *
 *  Created on: 12 juin 2020
 *      Author: Guillaume
 */

#include "main.h"
#include "pilote.h"
#include "corrector.h"

#define NB_MOTORS 4
#define COEF_DUTYCYCLE 99
uint16_t dutyCycle[NB_MOTORS] = {0};
double pid_consigne[NB_MOTORS] = {0};
uint16_t dutycycle_Motor1, dutycycle_Motor2, dutycycle_Motor3, dutycycle_Motor4;

void MOTORS_update(CORRECTOR_pid_out pid_out){

	pid_consigne[0] = pid_out.pid_output_WheelMotor1_rpm;
	pid_consigne[1] = pid_out.pid_output_WheelMotor2_rpm;
	pid_consigne[2] = pid_out.pid_output_WheelMotor3_rpm;
	pid_consigne[3] = pid_out.pid_output_WheelMotor4_rpm;

	// on major la correction du PID
	for (uint8_t motor = 0; motor < NB_MOTORS; motor++){
		if(pid_consigne[motor] > pid_outputMaxP) {
			pid_consigne[motor] = pid_outputMaxP;
		}
		else if(pid_consigne[motor] < pid_outputMaxN) {
			pid_consigne[motor] = pid_outputMaxN;
		}
		else {
			pid_consigne[motor] = pid_consigne[motor];
		}
	}
	// on transforme la consigne du PID en dutycycle avec une valeur absolue et un coefficient
	for (uint8_t motor = 0; motor < NB_MOTORS; motor++){
		if(pid_consigne[motor] < 0) {
			dutyCycle[motor] = (uint16_t)(-pid_consigne[motor] * COEF_DUTYCYCLE);
		}
		else {
			dutyCycle[motor] = (uint16_t)(pid_consigne[motor] * COEF_DUTYCYCLE);
		}
	}

	//on major le dutycycle
	for (uint8_t motor = 0; motor < NB_MOTORS; motor++){
		if(dutyCycle[motor] > DUTYCYCLE_MAX) {
			dutyCycle[motor] = DUTYCYCLE_MAX;
		}
		else {
			dutyCycle[motor] = dutyCycle[motor];
		}
	}
	// on applique le dutycycle
	//	if(pid_consigne[0] > 0) {
	//		htim10.Instance->CCR1 = dutyCycle[0];
	//		htim11.Instance->CCR1 = 0;
	//	}
	//	else if(pid_consigne[0] < 0) {
	//		htim10.Instance->CCR1 = 0;
	//		htim11.Instance->CCR1 = dutyCycle[0];
	//	}
	//	else {
	//		htim10.Instance->CCR1 = 0;
	//		htim11.Instance->CCR1 = 0;
	//	}
	//
	//	if(pid_consigne[1] > 0) {
	//		htim9.Instance->CCR1 = dutyCycle[1];
	//		htim9.Instance->CCR2 = 0;
	//	}
	//	else if(pid_consigne[1] < 0) {
	//		htim9.Instance->CCR1 = 0;
	//		htim9.Instance->CCR2 = dutyCycle[1];
	//	}
	//	else {
	//		htim9.Instance->CCR1 = 0;
	//		htim9.Instance->CCR2 = 0;
	//	}
	if(pid_consigne[0] > 0) {
		htim10.Instance->CCR1 = 0;
		htim11.Instance->CCR1 = dutyCycle[0];
	}
	else if(pid_consigne[0] < 0) {
		htim10.Instance->CCR1 = dutyCycle[0];
		htim11.Instance->CCR1 = 0;
	}
	else {
		htim10.Instance->CCR1 = 0;
		htim11.Instance->CCR1 = 0;
	}

	if(pid_consigne[1] > 0) {
		htim9.Instance->CCR1 = 0;
		htim9.Instance->CCR2 = dutyCycle[1];
	}
	else if(pid_consigne[1] < 0) {
		htim9.Instance->CCR1 = dutyCycle[1];
		htim9.Instance->CCR2 = 0;
	}
	else {
		htim9.Instance->CCR1 = 0;
		htim9.Instance->CCR2 = 0;
	}


	if(pid_consigne[2] > 0) {
		htim13.Instance->CCR1 = dutyCycle[2];
		htim14.Instance->CCR1 = 0;
	}
	else if(pid_consigne[2] < 0) {
		htim13.Instance->CCR1 = 0;
		htim14.Instance->CCR1 = dutyCycle[2];
	}
	else {
		htim13.Instance->CCR1 = 0;
		htim14.Instance->CCR1 = 0;
	}

	if(pid_consigne[3] > 0) {
		htim8.Instance->CCR3 = dutyCycle[3];
		htim8.Instance->CCR4 = 0;
	}
	else if(pid_consigne[3] < 0) {
		htim8.Instance->CCR3 = 0;
		htim8.Instance->CCR4 = dutyCycle[3];
	}
	else {
		htim8.Instance->CCR3 = 0;
		htim8.Instance->CCR4 = 0;
	}

}
