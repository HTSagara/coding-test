import { ref, watch } from 'vue'
import axios from 'axios'

export default function useUserForm(props, emit) {
  const user = ref({ ...props.user })

  // Watch for user prop changes and update local ref
  watch(
    () => props.user,
    (newUser) => {
      user.value = { ...newUser }
    },
    { deep: true },
  )

  const save = async () => {
    try {
      const userData = { ...user.value }
      delete userData._id // Remove _id before sending data

      if (props.isEditing) {
        await axios.put(`http://localhost:8000/api/users/${user.value._id}`, userData)
      } else {
        const response = await axios.post('http://localhost:8000/api/users', userData)
        emit('save', { ...userData, _id: response.data._id }) // Update frontend list
      }

      emit('close') // Close modal after saving
    } catch (error) {
      console.error('Error saving user:', error)
    }
  }

  return { user, save }
}
