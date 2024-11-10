#include "robot.h"

Robot::Robot(float a_max, float w_max): A_MAX(a_max), W_MAX(w_max), tcurve(a_max, w_max)
{
    printf("Robot initialization done\n");
}

Robot::~Robot()
{
    if (this->phi_vals != nullptr)
    {
        free(this->phi_vals);
        this->phi_vals = nullptr;
        printf("Memory for phi_vals deallocated in destructor\n");
    }
}
void Robot::recalculate(float phi_needed)
{
    printf("Recalculation process started\n");
    this->tcurve.set_phi(phi_needed);
    this->allocate_vector(this->tcurve.get_k_max());
    for (int i = 0; i < this->tcurve.get_k_max(); i++)
    {
        this->tcurve.curve_point(i * this->DT, &this->phi_vals[i]);
    }
}
void Robot::print_info()
{
    printf("Robot A_MAX: %.1f, W_MAX: %.1f\n", this->A_MAX, this->W_MAX);
    if (this->phi_vals != nullptr)
    {
        for (int i = 0; i < this->tcurve.get_k_max(); i++)
        {
            printf("phi val[%d]: %.2f\n", i, this->phi_vals[i]);
        }
    }
}

void Robot::save_info(const char* file_name)
{
    FILE *file = fopen(file_name, "w");
    if (file == nullptr)
    {
        printf("Failed to open file for writing!\n");
        return;
    }

    fprintf(file, "time,phi_val\n");

    for (int i = 0; i < this->tcurve.get_k_max(); i++)
    {
        float time = this->DT * i;
        fprintf(file, "%.5f,%.5f\n", time, this->phi_vals[i]);
    }

    fclose(file);
    printf("Data saved to %s\n", file_name);
}

void Robot::allocate_vector(int k)
{
    printf("Memory allocation for phi vector started\n");
    if (this->phi_vals != nullptr)
    {
        free(this->phi_vals);
        this->phi_vals = nullptr;
    }

    this->phi_vals = (float *)malloc(k * sizeof(float));
    if (this->phi_vals == nullptr)
    {
        printf("Memory allocation failed!\n");
        return;
    }
    printf("Memory allocated Done\n");
}