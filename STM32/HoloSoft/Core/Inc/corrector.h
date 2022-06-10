/*
 * corrector.h
 *
 *  Created on: 12 juin 2020
 *      Author: Guillaume
 */

#ifndef INC_CORRECTOR_H_
#define INC_CORRECTOR_H_

#include "pilote.h"
#include "odometry.h"

typedef struct{
	double pid_output_WheelMotor1_rpm;
	double pid_output_WheelMotor2_rpm;
	double pid_output_WheelMotor3_rpm;
	double pid_output_WheelMotor4_rpm;

}CORRECTOR_pid_out;
/**
 *
 * \param wheel
 * \param wheel_speed
 */
void CORRECTOR_pid(ODOMETRY_speed_wheel wheel, PILOTE_target_speed wheel_speed);

typedef struct {

	/* Controller gains */
	float Kp;
	float Ki;
	float Kd;

	/* Derivative low-pass filter time constant */
	float tau;

	/* Output limits */
	float limMin;
	float limMax;

	/* Integrator limits */
	float limMinInt;
	float limMaxInt;

	/* Sample time (in seconds) */
	float T;

	/* Controller "memory" */
	float integrator;
	float prevError;			/* Required for integrator */
	float differentiator;
	float prevMeasurement;		/* Required for differentiator */

	/* Controller output */
	float out;

} PIDController;

void  PIDController_Init(PIDController *pid);
float PIDController_Update(PIDController *pid, float setpoint, float measurement);

#endif /* INC_CORRECTOR_H_ */
