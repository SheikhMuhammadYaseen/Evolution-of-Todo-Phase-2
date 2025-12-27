'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    // Check if user has token
    const token = localStorage.getItem('access_token')

    if (token) {
      router.push('/dashboard')
    } else {
      router.push('/signin')
    }
  }, [router])

  return (
    <div className="flex min-h-screen items-center justify-center">
      <p>Loading...</p>
    </div>
  )
}
