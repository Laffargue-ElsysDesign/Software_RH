/*
 * corrector.c
 *
 *  Created on: 12 juin 2020
 *      Author: Guillaume
 */


#include "main.h"
#include "corrector.h"
#include "motors.h"
#include "debug.h"


// **** Variable pour le PID en vitesse (RPM) sur la roue
static double pid_error_WheelMotor1_rpm, pid_error_WheelMotor2_rpm, pid_error_WheelMotor3_rpm, pid_error_WheelMotor4_rpm;
static double pid_lasterror_WheelMotor1_rpm, pid_lasterror_WheelMotor2_rpm, pid_lasterror_WheelMotor3_rpm, pid_lasterror_WheelMotor4_rpm;
static double pid_lastmeasure_WheelMotor1_rpm, pid_lastmeasure_WheelMotor2_rpm, pid_lastmeasure_WheelMotor3_rpm, pid_lastmeasure_WheelMotor4_rpm;
//static double pid_input_WheelMotor1_rpm, pid_input_WheelMotor2_rpm, pid_input_WheelMotor3_rpm, pid_input_WheelMotor4_rpm;
static double pid_integral_WheelMotor1_rpm, pid_integral_WheelMotor2_rpm, pid_integral_WheelMotor3_rpm, pid_integral_WheelMotor4_rpm;
static double pid_derivate_WheelMotor1_rpm, pid_derivate_WheelMotor2_rpm, pid_derivate_WheelMotor3_rpm, pid_derivate_WheelMotor4_rpm;
//static double pid_differentiator_WheelMotor1_rpm, pid_differentiator_WheelMotor2_rpm, pid_differentiator_WheelMotor3_rpm, pid_differentiator_WheelMotor4_rpm;

CORRECTOR_pid_out pid_out;

//PIDController pid;

/*PIDController pid1
PIDController pid2
PIDController pid3
PIDController pid3*/

void CORRECTOR_pid(ODOMETRY_speed_wheel wheel, PILOTE_target_speed wheel_speed){

	if(PID_ON) {
		pid_error_WheelMotor1_rpm = wheel_speed.target_WheelMotor1_rpm - wheel.speed_WheelMotor1_rpm;
		pid_error_WheelMotor2_rpm = wheel_speed.target_WheelMotor2_rpm - wheel.speed_WheelMotor2_rpm;
		pid_error_WheelMotor3_rpm = wheel_speed.target_WheelMotor3_rpm - wheel.speed_WheelMotor3_rpm;
		pid_error_WheelMotor4_rpm = wheel_speed.target_WheelMotor4_rpm - wheel.speed_WheelMotor4_rpm;

		pid_integral_WheelMotor1_rpm = pid_integral_WheelMotor1_rpm + ((pid_error_WheelMotor1_rpm + pid_lasterror_WheelMotor1_rpm)*pid_KI_WheelMotor1_rpm*SAMPLING_TIME)/2;
		pid_integral_WheelMotor2_rpm = pid_integral_WheelMotor2_rpm + ((pid_error_WheelMotor2_rpm + pid_lasterror_WheelMotor1_rpm)*pid_KI_WheelMotor1_rpm*SAMPLING_TIME)/2;
		pid_integral_WheelMotor3_rpm = pid_integral_WheelMotor3_rpm + ((pid_error_WheelMotor3_rpm + pid_lasterror_WheelMotor1_rpm)*pid_KI_WheelMotor1_rpm*SAMPLING_TIME)/2;
		pid_integral_WheelMotor4_rpm = pid_integral_WheelMotor4_rpm + ((pid_error_WheelMotor4_rpm + pid_lasterror_WheelMotor1_rpm)*pid_KI_WheelMotor1_rpm*SAMPLING_TIME)/2;

		/* Anti-wind-up via integrator clamping */
		if (pid_integral_WheelMotor1_rpm > PID_LIM_MAX_INT) {

			pid_integral_WheelMotor1_rpm = PID_LIM_MAX_INT;

		} else if (pid_integral_WheelMotor1_rpm < PID_LIM_MIN_INT) {

			pid_integral_WheelMotor1_rpm = PID_LIM_MIN_INT;

		}

		if (pid_integral_WheelMotor2_rpm > PID_LIM_MAX_INT) {

			pid_integral_WheelMotor2_rpm = PID_LIM_MAX_INT;

		} else if (pid_integral_WheelMotor2_rpm < PID_LIM_MIN_INT) {

			pid_integral_WheelMotor2_rpm = PID_LIM_MIN_INT;

		}

		if (pid_integral_WheelMotor3_rpm > PID_LIM_MAX_INT) {

			pid_integral_WheelMotor3_rpm = PID_LIM_MAX_INT;

		} else if (pid_integral_WheelMotor3_rpm < PID_LIM_MIN_INT) {

			pid_integral_WheelMotor3_rpm = PID_LIM_MIN_INT;

		}

		if (pid_integral_WheelMotor4_rpm > PID_LIM_MAX_INT) {

			pid_integral_WheelMotor4_rpm = PID_LIM_MAX_INT;

		} else if (pid_integral_WheelMotor4_rpm < PID_LIM_MIN_INT) {

			pid_integral_WheelMotor4_rpm = PID_LIM_MIN_INT;

		}



		pid_derivate_WheelMotor1_rpm = -(2.0f * pid_KD_WheelMotor1_rpm * (wheel.speed_WheelMotor1_rpm - pid_lastmeasure_WheelMotor1_rpm)	/* Note: derivative on measurement, therefore minus sign in front of equation! */
                						+ (2.0f * PID_TAU - SAMPLING_TIME) * pid_derivate_WheelMotor1_rpm)
                						/ (2.0f * PID_TAU + SAMPLING_TIME);
		pid_derivate_WheelMotor2_rpm = -(2.0f * pid_KD_WheelMotor2_rpm * (wheel.speed_WheelMotor2_rpm - pid_lastmeasure_WheelMotor2_rpm)	/* Note: derivative on measurement, therefore minus sign in front of equation! */
										+ (2.0f * PID_TAU - SAMPLING_TIME) * pid_derivate_WheelMotor2_rpm)
										/ (2.0f * PID_TAU + SAMPLING_TIME);
		pid_derivate_WheelMotor3_rpm = -(2.0f * pid_KD_WheelMotor3_rpm * (wheel.speed_WheelMotor3_rpm - pid_lastmeasure_WheelMotor3_rpm)	/* Note: derivative on measurement, therefore minus sign in front of equation! */
										+ (2.0f * PID_TAU - SAMPLING_TIME) * pid_derivate_WheelMotor3_rpm)
										/ (2.0f * PID_TAU + SAMPLING_TIME);
		pid_derivate_WheelMotor4_rpm = -(2.0f * pid_KD_WheelMotor4_rpm * (wheel.speed_WheelMotor4_rpm - pid_lastmeasure_WheelMotor4_rpm)	/* Note: derivative on measurement, therefore minus sign in front of equation! */
										+ (2.0f * PID_TAU - SAMPLING_TIME) * pid_derivate_WheelMotor4_rpm)
										/ (2.0f * PID_TAU + SAMPLING_TIME);


		pid_out.pid_output_WheelMotor1_rpm = (pid_KP_WheelMotor1_rpm * pid_error_WheelMotor1_rpm) + (pid_integral_WheelMotor1_rpm) + (pid_derivate_WheelMotor1_rpm);
		pid_out.pid_output_WheelMotor2_rpm = (pid_KP_WheelMotor2_rpm * pid_error_WheelMotor2_rpm) + (pid_integral_WheelMotor2_rpm) + (pid_derivate_WheelMotor2_rpm);
		pid_out.pid_output_WheelMotor3_rpm = (pid_KP_WheelMotor3_rpm * pid_error_WheelMotor3_rpm) + (pid_integral_WheelMotor3_rpm) + (pid_derivate_WheelMotor3_rpm);
		pid_out.pid_output_WheelMotor4_rpm = (pid_KP_WheelMotor4_rpm * pid_error_WheelMotor4_rpm) + (pid_integral_WheelMotor4_rpm) + (pid_derivate_WheelMotor4_rpm);



		pid_lasterror_WheelMotor1_rpm = pid_error_WheelMotor1_rpm;
		pid_lasterror_WheelMotor2_rpm = pid_error_WheelMotor2_rpm;
		pid_lasterror_WheelMotor3_rpm = pid_error_WheelMotor3_rpm;
		pid_lasterror_WheelMotor4_rpm = pid_error_WheelMotor4_rpm;


		pid_lastmeasure_WheelMotor1_rpm = wheel.speed_WheelMotor1_rpm;
		pid_lastmeasure_WheelMotor2_rpm = wheel.speed_WheelMotor2_rpm;
		pid_lastmeasure_WheelMotor3_rpm = wheel.speed_WheelMotor3_rpm;
		pid_lastmeasure_WheelMotor4_rpm = wheel.speed_WheelMotor4_rpm;

	}
	else {
		pid_out.pid_output_WheelMotor1_rpm =  wheel_speed.target_WheelMotor1_rpm;
		pid_out.pid_output_WheelMotor2_rpm =  wheel_speed.target_WheelMotor2_rpm;
		pid_out.pid_output_WheelMotor3_rpm =  wheel_speed.target_WheelMotor3_rpm;
		pid_out.pid_output_WheelMotor4_rpm =  wheel_speed.target_WheelMotor4_rpm;
	}

	//DEBUG_update_corrector(wheel_speed.target_WheelMotor1_rpm, pid_out.pid_output_WheelMotor1_rpm, pid_out.pid_output_WheelMotor2_rpm, pid_out.pid_output_WheelMotor3_rpm, pid_error_WheelMotor1_rpm , pid_error_WheelMotor2_rpm, pid_error_WheelMotor3_rpm, pid_error_WheelMotor4_rpm, wheel.speed_WheelMotor1_rpm, wheel.speed_WheelMotor2_rpm, wheel.speed_WheelMotor3_rpm, wheel.speed_WheelMotor4_rpm);

	MOTORS_update(pid_out);

}
/*
void PIDController_Init(PIDController *pid) {

	/* Clear controller variables
	pid->integrator = 0.0f;
	pid->prevError  = 0.0f;

	pid->differentiator  = 0.0f;
	pid->prevMeasurement = 0.0f;

	pid->out = 0.0f;

}

void Init_corrector(){
	PIDController pid = { PID_KP, PID_KI, PID_KD,
	                          PID_TAU,
	                          PID_LIM_MIN, PID_LIM_MAX,
				  PID_LIM_MIN_INT, PID_LIM_MAX_INT,
	                          SAMPLE_TIME_S };

	    PIDController_Init(&pid);
}

float PIDController_Update(PIDController *pid, PILOTE_target_speed setpoint, ODOMETRY_speed_wheel measurement) {

	/*
	* Error signal

	pid_error_WheelMotor1_rpm = setpoint.target_WheelMotor1_rpm - measurement.speed_WheelMotor1_rpm;
	pid_error_WheelMotor2_rpm = setpoint.target_WheelMotor2_rpm - measurement.speed_WheelMotor2_rpm;
	pid_error_WheelMotor3_rpm = setpoint.target_WheelMotor3_rpm - measurement.speed_WheelMotor3_rpm;
	pid_error_WheelMotor4_rpm = setpoint.target_WheelMotor4_rpm - measurement.speed_WheelMotor4_rpm;

	/*
	* Proportional

    double proportional1 = pid->Kp1 * pid_error_WheelMotor1_rpm;
    double proportional1 = pid->Kp1 * pid_error_WheelMotor1_rpm;
    double proportional1 = pid->Kp1 * pid_error_WheelMotor1_rpm;
    double proportional1 = pid->Kp1 * pid_error_WheelMotor1_rpm;


	/*
	* Integral

    pid->integrator = pid->integrator + 0.5f * pid->Ki * pid->T * (error + pid->prevError);

	/* Anti-wind-up via integrator clamping
    if (pid->integrator > pid->limMaxInt) {

        pid->integrator = pid->limMaxInt;

    } else if (pid->integrator < pid->limMinInt) {

        pid->integrator = pid->limMinInt;

    }


	/*
	* Derivative (band-limited differentiator)


    pid->differentiator = -(2.0f * pid->Kd * (measurement - pid->prevMeasurement)	/* Note: derivative on measurement, therefore minus sign in front of equation!
                        + (2.0f * pid->tau - pid->T) * pid->differentiator)
                        / (2.0f * pid->tau + pid->T);


	/*
	* Compute output and apply limits

    pid->out = proportional + pid->integrator + pid->differentiator;

    /*if (pid->out > pid->limMax) {

        pid->out = pid->limMax;

    } else if (pid->out < pid->limMin) {

        pid->out = pid->limMin;

    }*/

	/* Store error and measurement for later use
    pid->prevError       = error;
    pid->prevMeasurement = measurement;

	/* Return controller output
    return pid->out;

}*/
