//frontend/src/composables/useUserDetail.js
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default function useUserDetail(userId) {
  const router = useRouter()
  const user = ref({})
  const editedUser = ref({})
  const loading = ref(true)
  const error = ref(null)
  const showEditModal = ref(false)
  const showDeleteConfirm = ref(false)

  const fetchUser = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/users/${userId}`)
      user.value = {
        ...response.data,
        roles: Array.isArray(response.data.roles) ? response.data.roles : [response.data.roles],
        preferences: response.data.preferences || { timezone: 'N/A' },
      }
    } catch (err) {
      error.value = 'Failed to fetch user details'
    } finally {
      loading.value = false
    }
  }

  const formatDate = (timestamp) => {
    return timestamp ? new Date(timestamp * 1000).toLocaleString() : 'N/A'
  }

  const openEditModal = () => {
    editedUser.value = { ...user.value }
    showEditModal.value = true
  }

  const handleSave = async () => {
    try {
      await axios.put(`http://localhost:8000/api/users/${userId}`, editedUser.value)
      user.value = editedUser.value
      showEditModal.value = false
      await fetchUser()
    } catch (err) {
      error.value = 'Failed to update user'
      console.error('Error updating user:', err)
    }
  }

  const confirmDelete = () => {
    showDeleteConfirm.value = true
  }

  const deleteUser = async () => {
    try {
      await axios.delete(`http://localhost:8000/api/users/${userId}`)
      router.push('/')
    } catch (err) {
      error.value = 'Failed to delete user'
      console.error('Error deleting user:', err)
    } finally {
      showDeleteConfirm.value = false
    }
  }

  onMounted(fetchUser)

  return {
    user,
    editedUser,
    loading,
    error,
    showEditModal,
    showDeleteConfirm,
    formatDate,
    openEditModal,
    handleSave,
    confirmDelete,
    deleteUser,
  }
}
