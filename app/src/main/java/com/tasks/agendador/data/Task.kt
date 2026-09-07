package com.seu.agendador.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "tasks")
data class Task(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val title: String,
    val description: String,
    val priority: String = "Média", // Alta, Média, Baixa
    val timeInMillis: Long, // Horário do alarme
    val isCompleted: Boolean = false
)