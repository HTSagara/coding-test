<template>
  <v-dialog v-model="isOpen" max-width="500px" persistent>
    <v-card>
      <v-card-title>
        <span class="text-h5">{{ isEditing ? 'Edit User' : 'Create User' }}</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form">
          <v-text-field v-model="user.username" label="Username" required></v-text-field>

          <v-text-field
            v-model="user.roles"
            label="Roles (comma separated)"
            hint="Example: admin, editor"
            persistent-hint
          ></v-text-field>

          <v-text-field v-model="user.preferences.timezone" label="Timezone"></v-text-field>

          <v-checkbox v-model="user.active" label="Active"></v-checkbox>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="grey darken-1" text @click="$emit('close')">Cancel</v-btn>
        <v-btn color="blue darken-1" text @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import useUserForm from '@/composables/useUserForm'

export default {
  props: ['isOpen', 'user', 'isEditing'],
  emits: ['close', 'save'],
  setup(props, { emit }) {
    return useUserForm(props, emit)
  },
}
</script>
