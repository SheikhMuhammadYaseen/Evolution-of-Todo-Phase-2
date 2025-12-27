'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { ApiClient } from '@/lib/api-client'
import { Task, TaskCreate } from '@/lib/types'
import TaskList from '@/components/TaskList'
import TaskForm from '@/components/TaskForm'
import Header from '@/components/Header'

export default function DashboardPage() {
  const router = useRouter()
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [submitLoading, setSubmitLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const token = localStorage.getItem('access_token')

    if (!token) {
      router.push('/signin')
      return
    }

    loadTasks(token)
  }, [router])

  const loadTasks = async (token: string) => {
    try {
      setLoading(true)
      const taskList = await ApiClient.get<Task[]>('/api/tasks', token)
      setTasks(taskList)
    } catch (err: any) {
      if (err.message.includes('Invalid') || err.message.includes('expired')) {
        localStorage.removeItem('access_token')
        router.push('/signin')
      } else {
        setError('Failed to load tasks')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleAddTask = async (taskData: TaskCreate) => {
    const token = localStorage.getItem('access_token')
    if (!token) return

    try {
      setSubmitLoading(true)
      const newTask = await ApiClient.post<Task>('/api/tasks', taskData, token)
      setTasks([newTask, ...tasks])
    } catch (err: any) {
      setError(err.message || 'Failed to create task')
    } finally {
      setSubmitLoading(false)
    }
  }

  const handleToggle = async (id: number) => {
    const token = localStorage.getItem('access_token')
    if (!token) return

    try {
      const updatedTask = await ApiClient.patch<Task>(
        `/api/tasks/${id}/complete`,
        token
      )
      setTasks(tasks.map((t) => (t.id === id ? updatedTask : t)))
    } catch (err: any) {
      setError(err.message || 'Failed to update task')
    }
  }

  const handleUpdate = async (id: number, title: string, description?: string) => {
    const token = localStorage.getItem('access_token')
    if (!token) return

    try {
      const updatedTask = await ApiClient.put<Task>(
        `/api/tasks/${id}`,
        { title, description },
        token
      )
      setTasks(tasks.map((t) => (t.id === id ? updatedTask : t)))
    } catch (err: any) {
      setError(err.message || 'Failed to update task')
    }
  }

  const handleDelete = async (id: number) => {
    const token = localStorage.getItem('access_token')
    if (!token) return

    if (!confirm('Are you sure you want to delete this task?')) return

    try {
      await ApiClient.delete(`/api/tasks/${id}`, token)
      setTasks(tasks.filter((t) => t.id !== id))
    } catch (err: any) {
      setError(err.message || 'Failed to delete task')
    }
  }

  if (loading) {
    return (
      <div>
        <Header />
        <div className="flex min-h-screen items-center justify-center">
          <p>Loading tasks...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-4 rounded bg-red-50 p-3 text-sm text-red-600">
            {error}
          </div>
        )}

        <div className="space-y-8">
          <TaskForm onSubmit={handleAddTask} loading={submitLoading} />

          <div>
            <h2 className="mb-4 text-xl font-semibold">Your Tasks</h2>
            <TaskList
              tasks={tasks}
              onToggle={handleToggle}
              onUpdate={handleUpdate}
              onDelete={handleDelete}
            />
          </div>
        </div>
      </main>
    </div>
  )
}
