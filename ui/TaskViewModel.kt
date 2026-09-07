package com.seu.agendador.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import androidx.work.Data
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import com.seu.agendador.data.AppDatabase
import com.seu.agendador.data.Task
import com.seu.agendador.worker.TaskWorker
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import java.util.concurrent.TimeUnit

class TaskViewModel(application: Application) : AndroidViewModel(application) {
    private val dao = AppDatabase.getDatabase(application).taskDao()
    private val workManager = WorkManager.getInstance(application)

    val tasks = dao.getAllTasks().stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    fun addTask(title: String, desc: String, priority: String, delayInMillis: Long) {
        viewModelScope.launch {
            val task = Task(title = title, description = desc, priority = priority, timeInMillis = System.currentTimeMillis() + delayInMillis)
            dao.insertTask(task)
            scheduleNotification(title, desc, delayInMillis)
        }
    }

    fun toggleComplete(task: Task) {
        viewModelScope.launch { dao.updateTask(task.copy(isCompleted = !task.isCompleted)) }
    }

    fun deleteTask(task: Task) {
        viewModelScope.launch { dao.deleteTask(task) }
    }

    private fun scheduleNotification(title: String, desc: String, delay: Long) {
        val data = Data.Builder().putString("title", title).putString("desc", desc).build()
        val request = OneTimeWorkRequestBuilder<TaskWorker>()
            .setInitialDelay(delay, TimeUnit.MILLISECONDS)
            .setInputData(data)
            .build()
        workManager.enqueue(request)
    }
}