<template>
  <main v-if="!isAuthenticated" class="login-page" :class="{ 'theme-dark': themeDark }">
    <section class="login-card">
      <button
        class="theme-toggle login-theme-toggle"
        type="button"
        :aria-label="themeDark ? 'Switch to light theme' : 'Switch to dark theme'"
        @click="toggleTheme"
      >
        <span aria-hidden="true">{{ themeDark ? '☀' : '◐' }}</span>
        <span>{{ themeDark ? 'Light' : 'Dark' }}</span>
      </button>
      <a class="brand-mark brand-mark-large" href="#" aria-label="MyDigitalWorld home">MVS</a>
      <p class="eyebrow">MY DIGITAL WORKSPACE</p>
      <h1>Welcome back</h1>
      <p class="muted">Enter your password to open your content workspace.</p>
      <form class="login-form" @submit.prevent="login">
        <label for="login-password">Password</label>
        <input
          id="login-password"
          v-model="loginPassword"
          type="password"
          autocomplete="current-password"
          placeholder="Enter password"
          required
        >
        <p v-if="loginError" class="form-error" role="alert">{{ loginError }}</p>
        <button class="button button-primary button-wide" type="submit">Continue</button>
      </form>
      <p class="login-footnote">Your session automatically ends after one hour.</p>
    </section>
  </main>

  <div v-else class="app-shell" :class="{ 'sidebar-is-closed': !sidebarOpen, 'theme-dark': themeDark }">
    <button
      v-if="isMobile && sidebarOpen"
      class="sidebar-backdrop"
      type="button"
      aria-label="Close navigation menu"
      @click="closeSidebar"
    />

    <aside
      id="workspace-sidebar"
      class="sidebar"
      :class="{ 'sidebar-is-closed': !sidebarOpen }"
      :aria-hidden="!sidebarOpen"
    >
      <div class="sidebar-heading">
        <a class="brand" href="#" @click.prevent="selectHome">
          <span class="brand-mark">MVS</span>
          <span class="brand-name">MyDigitalWorld</span>
        </a>
        <button class="icon-button sidebar-close" type="button" aria-label="Close menu" @click="closeSidebar">×</button>
      </div>

      <div class="sidebar-section-heading">
        <span>YOUR WORKSPACE</span>
        <button class="icon-button" type="button" aria-label="Create tab" title="Create tab" @click="openNameDialog('create-tab')">+</button>
      </div>

      <div class="navigation-tree">
        <div v-if="loadingTabs" class="tree-empty">Loading your tabs…</div>
        <div v-else-if="tabs.length === 0" class="tree-empty">
          <span>No tabs yet</span>
          <button class="text-button" type="button" @click="openNameDialog('create-tab')">Create your first tab</button>
        </div>
        <section v-for="tab in tabs" :key="tab.id" class="tree-group">
          <div class="tree-row" :class="{ 'tree-row-active': selectedTabId === tab.id }">
            <button class="tree-select" type="button" @click="selectTab(tab.id)">
              <span class="tree-chevron" aria-hidden="true">{{ selectedTabId === tab.id ? '⌄' : '›' }}</span>
              <span class="tree-label">{{ tab.name }}</span>
            </button>
            <div class="tree-actions">
              <button v-if="editUnlocked" class="icon-button compact" type="button" :aria-label="`Rename ${tab.name}`" title="Rename tab" @click="openNameDialog('rename-tab', tab)">✎</button>
              <button v-if="editUnlocked" class="icon-button compact danger-on-hover" type="button" :aria-label="`Delete ${tab.name}`" title="Delete tab" @click="deleteTab(tab)">×</button>
            </div>
          </div>

          <div v-if="selectedTabId === tab.id" class="tree-children">
            <div v-for="frame in frames" :key="frame.id" class="tree-row frame-row" :class="{ 'tree-row-active': selectedFrameId === frame.id }">
              <button class="tree-select" type="button" @click="selectFrame(frame.id)">
                <span class="frame-indicator" aria-hidden="true"></span>
                <span class="tree-label">{{ frame.name }}</span>
              </button>
              <div class="tree-actions">
                <button v-if="editUnlocked" class="icon-button compact" type="button" :aria-label="`Rename ${frame.name}`" title="Rename frame" @click="openNameDialog('rename-frame', frame)">✎</button>
                <button v-if="editUnlocked" class="icon-button compact danger-on-hover" type="button" :aria-label="`Delete ${frame.name}`" title="Delete frame" @click="deleteFrame(frame)">×</button>
              </div>
            </div>
            <button class="tree-add-frame" type="button" @click="openNameDialog('create-frame')">
              <span aria-hidden="true">+</span> Add frame
            </button>
          </div>
        </section>
      </div>

      <div class="sidebar-footer">
        <span class="account-avatar" aria-hidden="true">MVS</span>
        <span class="account-label">My workspace</span>
        <button class="icon-button" type="button" title="Log out" aria-label="Log out" @click="logout">↪</button>
      </div>
    </aside>

    <section class="main-area">
      <header class="topbar">
        <button
          class="menu-toggle"
          type="button"
          :aria-label="sidebarOpen ? 'Close side menu' : 'Open side menu'"
          :aria-expanded="sidebarOpen"
          aria-controls="workspace-sidebar"
          @click="toggleSidebar"
        >
          <span aria-hidden="true">{{ sidebarOpen ? '‹' : '☰' }}</span>
          <span>{{ sidebarOpen ? 'Close menu' : 'Open menu' }}</span>
        </button>
        <div class="topbar-spacer"></div>
        <button class="theme-toggle" type="button" :aria-label="themeDark ? 'Switch to light theme' : 'Switch to dark theme'" @click="toggleTheme">
          <span aria-hidden="true">{{ themeDark ? '☀' : '◐' }}</span>
          <span>{{ themeDark ? 'Light' : 'Dark' }}</span>
        </button>
        <button
          class="edit-lock-button"
          :class="{ 'edit-lock-open': editUnlocked }"
          type="button"
          :aria-label="editUnlocked ? 'Lock editing and deleting' : 'Unlock editing and deleting'"
          @click="editUnlocked ? lockEditing() : openUnlockDialog()"
        >
          <span aria-hidden="true">{{ editUnlocked ? '♧' : '▣' }}</span>
          <span>{{ editUnlocked ? 'Unlocked' : 'Locked' }}</span>
        </button>
        <span class="session-indicator"><span class="status-dot"></span> Session active</span>
        <button class="button button-subtle logout-button" type="button" @click="logout">Log out</button>
      </header>

      <div class="content-scroll">
        <div v-if="errorMessage" class="alert alert-error" role="alert">
          <span>{{ errorMessage }}</span>
          <button class="icon-button" type="button" aria-label="Dismiss error" @click="errorMessage = ''">×</button>
        </div>
        <div v-if="noticeMessage" class="alert alert-success" role="status">{{ noticeMessage }}</div>

        <section v-if="!selectedTab" class="welcome-panel">
          <div class="welcome-icon" aria-hidden="true">✦</div>
          <p class="eyebrow">A PLACE FOR YOUR CONTENT</p>
          <h1>Build your digital world</h1>
          <p class="muted">Start by creating a tab. Add frames inside it, then choose a field type to organize your content.</p>
          <button class="button button-primary" type="button" @click="openNameDialog('create-tab')">Create your first tab</button>
        </section>

        <template v-else>
          <div class="page-heading">
            <div>
              <p class="breadcrumb">{{ selectedTab.name }}<span v-if="selectedFrame"> / {{ selectedFrame.name }}</span></p>
              <h1>{{ selectedFrame ? selectedFrame.name : selectedTab.name }}</h1>
              <p class="muted">
                <template v-if="selectedFrame">Manage the fields and content in this frame.</template>
                <template v-else>Create a frame in this tab, then add fields to it.</template>
              </p>
            </div>
            <button v-if="!isMobile && selectedTab" class="button button-subtle" type="button" @click="openNameDialog('create-frame')">
              <span aria-hidden="true">+</span> New frame
            </button>
          </div>

          <section v-if="!selectedFrame" class="empty-state card">
            <div class="empty-state-icon" aria-hidden="true">▧</div>
            <h2>This tab is ready for its first frame</h2>
            <p class="muted">Frames keep related fields together. Create a frame first, then select it to add content.</p>
            <button class="button button-primary" type="button" @click="openNameDialog('create-frame')">Create a frame</button>
          </section>

          <template v-else>
            <section class="add-field-panel card">
              <div>
                <p class="eyebrow">FRAME CONTENT</p>
                <h2>Add a field</h2>
                <p class="muted">Choose a field type to add it to <strong>{{ selectedFrame.name }}</strong>.</p>
              </div>
              <div class="field-create-control">
                <button
                  ref="fieldTypeTrigger"
                  class="field-type-trigger"
                  type="button"
                  role="combobox"
                  aria-label="Field type"
                  aria-haspopup="listbox"
                  aria-controls="field-type-menu"
                  :aria-expanded="fieldTypeMenuOpen"
                  @click="toggleFieldTypeMenu"
                  @keydown.down.prevent="openFieldTypeMenu"
                  @keydown.up.prevent="openFieldTypeMenu"
                >
                  <span>{{ fieldTypeLabel(newFieldType) }}</span>
                  <span aria-hidden="true">⌄</span>
                </button>
                <button class="button button-primary" type="button" @click="openFieldEditor()">Add field <span aria-hidden="true">+</span></button>
              </div>
            </section>

            <div class="fields-heading">
              <div>
                <h2>Fields</h2>
                <span class="count-pill">{{ fields.length }}</span>
              </div>
              <span v-if="loadingFields" class="muted small-text">Refreshing…</span>
            </div>

            <section v-if="loadingFields && fields.length === 0" class="card empty-fields">Loading fields…</section>
            <section v-else-if="fields.length === 0" class="card empty-fields">
              <div class="empty-state-icon" aria-hidden="true">＋</div>
              <h3>No fields in this frame</h3>
              <p class="muted">Use the field type selector above to add direct data, key–value pairs, or text with images.</p>
            </section>
            <section v-else class="field-list">
              <article v-for="field in fields" :key="field.id" class="field-card card">
                <div class="field-card-header">
                  <div class="field-title-group">
                    <span class="field-type-icon" aria-hidden="true">{{ fieldIcon(field.type) }}</span>
                    <div>
                      <p class="field-type-label">{{ fieldTypeLabel(field.type) }}</p>
                      <h3>{{ field.label }}</h3>
                    </div>
                  </div>
                  <div class="field-card-actions">
                    <button v-if="editUnlocked" class="button button-small button-subtle" type="button" @click="openFieldEditor(field)">Edit</button>
                    <button v-if="editUnlocked" class="button button-small button-danger" type="button" @click="deleteField(field)">Delete</button>
                  </div>
                </div>
                <div v-if="field.type === 'direct'" class="field-body direct-value">{{ field.value || 'No value entered.' }}</div>
                <dl v-else-if="field.type === 'keyValue'" class="key-value-list">
                  <template v-for="(pair, index) in field.pairs" :key="`${field.id}-${index}`">
                    <dt>{{ pair.key }}</dt>
                    <dd>{{ pair.value }}</dd>
                  </template>
                  <p v-if="!field.pairs?.length" class="muted">No key–value pairs.</p>
                </dl>
                <div v-else class="text-image-content">
                  <p v-if="field.text" class="field-body preserve-lines">{{ field.text }}</p>
                  <p v-else class="muted">No text entered.</p>
                  <div v-if="field.images?.length" class="image-grid">
                    <button v-for="image in field.images" :key="image.id" class="image-thumbnail" type="button" :aria-label="`Zoom ${image.name || 'uploaded image'}`" @click="openImage(image)">
                      <img :src="image.url" :alt="image.name || field.label">
                    </button>
                  </div>
                  <p v-if="field.imageIds?.length" class="image-count">{{ field.images?.length || 0 }} of {{ field.imageIds.length }} image(s) loaded</p>
                </div>
              </article>
            </section>
          </template>
        </template>
      </div>
    </section>

    <Teleport to="body">
      <div
        v-if="fieldTypeMenuOpen"
        ref="fieldTypeMenu"
        id="field-type-menu"
        class="field-type-menu"
        role="listbox"
        aria-label="Choose field type"
        :style="fieldTypeMenuStyle"
        @keydown.esc.prevent="closeFieldTypeMenu(true)"
      >
        <button
          v-for="option in fieldTypeOptions"
          :key="option.value"
          class="field-type-option"
          :class="{ 'field-type-option-active': newFieldType === option.value }"
          type="button"
          role="option"
          :aria-selected="newFieldType === option.value"
          @click="selectFieldType(option.value)"
        >
          <span class="field-type-option-icon" aria-hidden="true">{{ fieldIcon(option.value) }}</span>
          <span>{{ option.label }}</span>
          <span v-if="newFieldType === option.value" class="field-type-check" aria-hidden="true">✓</span>
        </button>
      </div>
    </Teleport>

    <div v-if="nameDialog.open" class="modal-backdrop" @click.self="closeNameDialog">
      <section class="modal-card" role="dialog" aria-modal="true" :aria-labelledby="'name-dialog-title'">
        <button class="modal-close icon-button" type="button" aria-label="Close dialog" @click="closeNameDialog">×</button>
        <p class="eyebrow">{{ nameDialogEyebrow }}</p>
        <h2 id="name-dialog-title">{{ nameDialogTitle }}</h2>
        <form class="modal-form" @submit.prevent="submitNameDialog">
          <label for="name-dialog-input">{{ nameDialogLabel }}</label>
          <input id="name-dialog-input" v-model="nameDialog.value" type="text" maxlength="80" required autofocus>
          <div class="modal-actions">
            <button class="button button-subtle" type="button" @click="closeNameDialog">Cancel</button>
            <button class="button button-primary" type="submit" :disabled="savingName">{{ savingName ? 'Saving…' : 'Save' }}</button>
          </div>
        </form>
      </section>
    </div>

    <div v-if="unlockDialogOpen" class="modal-backdrop" @click.self="closeUnlockDialog">
      <section class="modal-card unlock-card" role="dialog" aria-modal="true" aria-labelledby="unlock-title">
        <button class="modal-close icon-button" type="button" aria-label="Close dialog" @click="closeUnlockDialog">×</button>
        <p class="eyebrow">PROTECTED ACTIONS</p>
        <h2 id="unlock-title">Unlock editing</h2>
        <p class="muted unlock-description">Enter the edit password to enable rename and delete actions.</p>
        <form class="modal-form" @submit.prevent="unlockEditing">
          <label for="edit-password">Edit password</label>
          <input
            id="edit-password"
            v-model="unlockPassword"
            type="password"
            autocomplete="current-password"
            placeholder="Enter edit password"
            required
          >
          <p v-if="unlockError" class="form-error" role="alert">{{ unlockError }}</p>
          <div class="modal-actions">
            <button class="button button-subtle" type="button" @click="closeUnlockDialog">Cancel</button>
            <button class="button button-primary" type="submit">Unlock</button>
          </div>
        </form>
      </section>
    </div>

    <div v-if="fieldEditor.open" class="modal-backdrop editor-backdrop" @click.self="closeFieldEditor">
      <section class="modal-card field-editor" role="dialog" aria-modal="true" aria-labelledby="field-editor-title">
        <button class="modal-close icon-button" type="button" aria-label="Close editor" @click="closeFieldEditor">×</button>
        <p class="eyebrow">{{ fieldEditor.id ? 'EDIT FIELD' : 'NEW FIELD' }} · {{ fieldTypeLabel(fieldEditor.type) }}</p>
        <h2 id="field-editor-title">{{ fieldEditor.id ? 'Edit field' : 'Add a field' }}</h2>
        <form class="modal-form editor-form" @submit.prevent="saveField">
          <label for="field-label">Field name</label>
          <input id="field-label" v-model="fieldEditor.label" type="text" maxlength="100" placeholder="Give this field a name" required>

          <template v-if="fieldEditor.type === 'direct'">
            <label for="direct-value">Value</label>
            <textarea id="direct-value" v-model="fieldEditor.value" rows="5" placeholder="Enter a value"></textarea>
          </template>

          <template v-else-if="fieldEditor.type === 'keyValue'">
            <div class="subform-heading">
              <div><label>Key–value pairs</label><p class="muted small-text">Add one or more related values.</p></div>
              <button class="button button-small button-subtle" type="button" @click="addPair">+ Add pair</button>
            </div>
            <div v-for="(pair, index) in fieldEditor.pairs" :key="index" class="pair-editor">
              <input v-model="pair.key" type="text" maxlength="100" placeholder="Key" :aria-label="`Pair ${index + 1} key`">
              <input v-model="pair.value" type="text" maxlength="500" placeholder="Value" :aria-label="`Pair ${index + 1} value`">
              <button class="icon-button danger-on-hover" type="button" :aria-label="`Remove pair ${index + 1}`" @click="removePair(index)">×</button>
            </div>
          </template>

          <template v-else>
            <label for="text-value">Text</label>
            <textarea id="text-value" v-model="fieldEditor.text" rows="5" placeholder="Write something…"></textarea>
            <div class="subform-heading image-upload-heading">
              <div><label>Images <span class="muted small-text">({{ fieldEditor.images.length }}/10)</span></label><p class="muted small-text">JPEG, PNG, GIF or WebP. Up to 650 KiB per image.</p></div>
              <label class="button button-small button-subtle file-picker" :class="{ 'button-disabled': fieldEditor.images.length >= MAX_IMAGES }">
                + Add images
                <input type="file" accept="image/*" multiple :disabled="fieldEditor.images.length >= MAX_IMAGES" @change="addImages">
              </label>
            </div>
            <div v-if="fieldEditor.images.length" class="editor-image-grid">
              <div v-for="(image, index) in fieldEditor.images" :key="image.id || `${image.file?.name}-${index}`" class="editor-image">
                <button class="editor-image-preview" type="button" :aria-label="`Zoom ${image.name || 'image'}`" @click="openImage(image)">
                  <img :src="image.url" :alt="image.name || 'Image preview'">
                </button>
                <div class="editor-image-actions">
                  <span class="image-name" :title="image.name">{{ image.name }}</span>
                  <label class="text-button replace-picker">Replace<input type="file" accept="image/*" @change="replaceImage(index, $event)"></label>
                  <button class="text-button text-danger" type="button" @click="removeImage(index)">Remove</button>
                </div>
              </div>
            </div>
          </template>

          <p v-if="editorError" class="form-error" role="alert">{{ editorError }}</p>
          <div class="modal-actions editor-actions">
            <button class="button button-subtle" type="button" @click="closeFieldEditor">Cancel</button>
            <button class="button button-primary" type="submit" :disabled="savingField">{{ savingField ? 'Saving…' : 'Save field' }}</button>
          </div>
        </form>
      </section>
    </div>

    <div v-if="zoomedImage" class="modal-backdrop image-viewer-backdrop" role="presentation" @click.self="closeImage">
      <section class="image-viewer" role="dialog" aria-modal="true" aria-label="Image preview">
        <button class="viewer-close icon-button" type="button" aria-label="Close image preview" @click="closeImage">×</button>
        <img :src="zoomedImage.url" :alt="zoomedImage.name || 'Image preview'">
        <p v-if="zoomedImage.name" class="viewer-caption">{{ zoomedImage.name }}</p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import {
  collection,
  doc,
  getDoc,
  getDocs,
  onSnapshot,
  serverTimestamp,
  setDoc,
  writeBatch
} from 'firebase/firestore'
import { db } from '@/firebase'

const SESSION_KEY = 'mydigitalworld-session-expiry'
const SESSION_DURATION = 60 * 60 * 1000
const MAX_IMAGES = 10
const MAX_IMAGE_BYTES = 650 * 1024

const tabs = ref([])
const frames = ref([])
const fields = ref([])
const selectedTabId = ref('')
const selectedFrameId = ref('')
const sidebarOpen = ref(true)
const isMobile = ref(false)
const themeDark = ref(localStorage.getItem('mydigitalworld-theme') === 'dark')
const fieldTypeMenuOpen = ref(false)
const fieldTypeTrigger = ref(null)
const fieldTypeMenu = ref(null)
const fieldTypeMenuPosition = ref({ top: 0, left: 0, width: 0, maxHeight: 180 })
const editUnlocked = ref(false)
const unlockDialogOpen = ref(false)
const unlockPassword = ref('')
const unlockError = ref('')
const loadingTabs = ref(false)
const loadingFields = ref(false)
const savingName = ref(false)
const savingField = ref(false)
const errorMessage = ref('')
const noticeMessage = ref('')
const loginPassword = ref('')
const loginError = ref('')
const editorError = ref('')
const loginExpiry = ref(0)
const loginTimer = ref(null)
const tabsUnsubscribe = ref(null)
const framesUnsubscribe = ref(null)
const fieldsUnsubscribe = ref(null)
const fieldsLoadToken = ref(0)
const mobileQuery = ref(null)
const imageUrlCache = new Map()
const zoomedImage = ref(null)
const newFieldType = ref('direct')
const fieldTypeOptions = [
  { value: 'direct', label: 'Direct field' },
  { value: 'keyValue', label: 'Key–value field' },
  { value: 'textImages', label: 'Text and images' }
]

const isAuthenticated = ref(checkStoredSession())
const configuredPassword = process.env.VUE_APP_LOGIN_PASSWORD || 'Suresh@7989'
const configuredEditPassword = process.env.VUE_APP_EDIT_PASSWORD || 'MVS'

const selectedTab = computed(() => tabs.value.find(tab => tab.id === selectedTabId.value) || null)
const selectedFrame = computed(() => frames.value.find(frame => frame.id === selectedFrameId.value) || null)

const nameDialog = reactive({
  open: false,
  kind: '',
  id: '',
  value: ''
})

const fieldEditor = reactive({
  open: false,
  id: '',
  type: 'direct',
  label: '',
  value: '',
  pairs: [],
  text: '',
  images: [],
  originalImageIds: []
})

const nameDialogTitle = computed(() => ({
  'create-tab': 'Create a tab',
  'rename-tab': 'Rename tab',
  'create-frame': 'Create a frame',
  'rename-frame': 'Rename frame'
}[nameDialog.kind] || 'Name'))
const nameDialogEyebrow = computed(() => nameDialog.kind.includes('frame') ? 'FRAME' : 'TAB')
const nameDialogLabel = computed(() => nameDialog.kind.includes('frame') ? 'Frame name' : 'Tab name')
const fieldTypeMenuStyle = computed(() => ({
  top: `${fieldTypeMenuPosition.value.top}px`,
  left: `${fieldTypeMenuPosition.value.left}px`,
  width: `${fieldTypeMenuPosition.value.width}px`,
  maxHeight: `${fieldTypeMenuPosition.value.maxHeight}px`
}))

watch(themeDark, dark => {
  document.documentElement.dataset.theme = dark ? 'dark' : 'light'
  localStorage.setItem('mydigitalworld-theme', dark ? 'dark' : 'light')
}, { immediate: true })

function checkStoredSession() {
  const expiry = Number(sessionStorage.getItem(SESSION_KEY))
  if (Number.isFinite(expiry) && expiry > Date.now()) {
    loginExpiry.value = expiry
    return true
  }
  sessionStorage.removeItem(SESSION_KEY)
  return false
}

function clearLoginTimer() {
  if (loginTimer.value) {
    window.clearTimeout(loginTimer.value)
    loginTimer.value = null
  }
}

function scheduleLogout() {
  clearLoginTimer()
  const remaining = loginExpiry.value - Date.now()
  if (remaining <= 0) {
    logout(true)
    return
  }
  loginTimer.value = window.setTimeout(() => logout(true), remaining)
}

function login() {
  if (loginPassword.value !== configuredPassword) {
    loginError.value = 'That password is not correct. Please try again.'
    return
  }
  loginError.value = ''
  loginPassword.value = ''
  loginExpiry.value = Date.now() + SESSION_DURATION
  sessionStorage.setItem(SESSION_KEY, String(loginExpiry.value))
  isAuthenticated.value = true
  scheduleLogout()
}

function logout(expired = false) {
  sessionStorage.removeItem(SESSION_KEY)
  clearLoginTimer()
  editUnlocked.value = false
  closeUnlockDialog()
  loginExpiry.value = 0
  isAuthenticated.value = false
  selectedTabId.value = ''
  selectedFrameId.value = ''
  tabs.value = []
  frames.value = []
  fields.value = []
  closeFieldEditor()
  closeNameDialog()
  stopListeners()
  revokeImageUrls()
  if (expired) loginError.value = 'Your one-hour session expired. Please sign in again.'
}

function handleVisibilityChange() {
  if (document.visibilityState === 'visible' && isAuthenticated.value && loginExpiry.value <= Date.now()) {
    logout(true)
  }
}

function stopListeners() {
  if (tabsUnsubscribe.value) tabsUnsubscribe.value()
  if (framesUnsubscribe.value) framesUnsubscribe.value()
  if (fieldsUnsubscribe.value) fieldsUnsubscribe.value()
  tabsUnsubscribe.value = null
  framesUnsubscribe.value = null
  fieldsUnsubscribe.value = null
}

function revokeImageUrls() {
  imageUrlCache.forEach(image => URL.revokeObjectURL(image.url))
  imageUrlCache.clear()
}

function reportError(error, context) {
  console.error(context, error)
  errorMessage.value = `${context}: ${error.message || 'Please try again.'}`
}

function sortByCreatedAt(items) {
  return items.sort((a, b) => {
    const timeA = a.createdAt?.toMillis?.() || 0
    const timeB = b.createdAt?.toMillis?.() || 0
    return timeA - timeB || a.name.localeCompare(b.name)
  })
}

function startTabsListener() {
  loadingTabs.value = true
  tabsUnsubscribe.value = onSnapshot(
    collection(db, 'tabs'),
    snapshot => {
      tabs.value = sortByCreatedAt(snapshot.docs.map(item => ({ id: item.id, ...item.data() })))
      loadingTabs.value = false
      if (!tabs.value.some(tab => tab.id === selectedTabId.value)) {
        selectedTabId.value = tabs.value[0]?.id || ''
      }
    },
    error => {
      loadingTabs.value = false
      reportError(error, 'Could not load tabs')
    }
  )
}

function watchFrames(tabId) {
  if (framesUnsubscribe.value) framesUnsubscribe.value()
  if (fieldsUnsubscribe.value) fieldsUnsubscribe.value()
  framesUnsubscribe.value = null
  fieldsUnsubscribe.value = null
  frames.value = []
  fields.value = []
  selectedFrameId.value = ''
  revokeImageUrls()
  if (!tabId || !isAuthenticated.value) return

  framesUnsubscribe.value = onSnapshot(
    collection(db, 'tabs', tabId, 'frames'),
    snapshot => {
      frames.value = sortByCreatedAt(snapshot.docs.map(item => ({ id: item.id, ...item.data() })))
      if (!frames.value.some(frame => frame.id === selectedFrameId.value)) {
        selectedFrameId.value = frames.value[0]?.id || ''
      }
    },
    error => reportError(error, 'Could not load frames')
  )
}

function toImageUrl(id, data) {
  const cached = imageUrlCache.get(id)
  if (cached) return cached
  const binary = atob(data.data)
  const bytes = new Uint8Array(binary.length)
  for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index)
  const url = URL.createObjectURL(new Blob([bytes], { type: data.contentType || 'application/octet-stream' }))
  const image = { id, url, name: data.name || 'Uploaded image' }
  imageUrlCache.set(id, image)
  return image
}

async function hydrateFields(tabId, frameId, rawFields, token) {
  const hydrated = await Promise.all(rawFields.map(async field => {
    const images = await Promise.all((field.imageIds || []).map(async id => {
      const cached = imageUrlCache.get(id)
      if (cached) return cached
      const imageSnapshot = await getDoc(doc(db, 'tabs', tabId, 'images', id))
      if (!imageSnapshot.exists()) return null
      return toImageUrl(id, imageSnapshot.data())
    }))
    return { ...field, frameId, images: images.filter(Boolean) }
  }))
  if (token === fieldsLoadToken.value && selectedTabId.value === tabId && selectedFrameId.value === frameId) {
    fields.value = hydrated
    loadingFields.value = false
  }
}

function watchFields(tabId, frameId) {
  if (fieldsUnsubscribe.value) fieldsUnsubscribe.value()
  fieldsUnsubscribe.value = null
  fields.value = []
  loadingFields.value = Boolean(frameId)
  fieldsLoadToken.value += 1
  if (!tabId || !frameId || !isAuthenticated.value) {
    loadingFields.value = false
    return
  }
  fieldsUnsubscribe.value = onSnapshot(
    collection(db, 'tabs', tabId, 'frames', frameId, 'fields'),
    snapshot => {
      const token = fieldsLoadToken.value + 1
      fieldsLoadToken.value = token
      const rawFields = snapshot.docs.map(item => ({ id: item.id, ...item.data() }))
      hydrateFields(tabId, frameId, rawFields, token).catch(error => {
        loadingFields.value = false
        reportError(error, 'Could not load field images')
      })
    },
    error => {
      loadingFields.value = false
      reportError(error, 'Could not load fields')
    }
  )
}

watch(isAuthenticated, authenticated => {
  if (authenticated) {
    startTabsListener()
    scheduleLogout()
  } else {
    stopListeners()
  }
}, { immediate: true })

watch(selectedTabId, tabId => watchFrames(tabId))
watch(selectedFrameId, frameId => watchFields(selectedTabId.value, frameId))

function selectHome() {
  selectedTabId.value = ''
}

function selectTab(tabId) {
  selectedTabId.value = tabId
  if (isMobile.value) closeSidebar()
}

function selectFrame(frameId) {
  selectedFrameId.value = frameId
  if (isMobile.value) closeSidebar()
}

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

function closeSidebar() {
  sidebarOpen.value = false
}

function toggleTheme() {
  themeDark.value = !themeDark.value
}

function updateFieldTypeMenuPosition() {
  const trigger = fieldTypeTrigger.value
  if (!trigger || !fieldTypeMenuOpen.value) return
  const rect = trigger.getBoundingClientRect()
  const margin = 12
  const gap = 6
  const idealHeight = 3 * 44 + 14
  const viewportHeight = window.innerHeight
  const viewportWidth = window.innerWidth
  const below = Math.max(0, viewportHeight - rect.bottom - margin - gap)
  const above = Math.max(0, rect.top - margin - gap)
  const openAbove = below < Math.min(idealHeight, 120) && above > below
  const availableHeight = Math.max(0, Math.min(idealHeight, openAbove ? above : below))
  const height = Math.min(idealHeight, availableHeight)
  const width = Math.min(Math.max(rect.width, 220), Math.max(0, viewportWidth - margin * 2))
  const left = Math.min(Math.max(margin, rect.left), Math.max(margin, viewportWidth - width - margin))
  const top = openAbove
    ? Math.max(margin, rect.top - gap - height)
    : Math.min(rect.bottom + gap, Math.max(margin, viewportHeight - height - margin))
  fieldTypeMenuPosition.value = { top, left, width, maxHeight: Math.max(0, availableHeight) }
}

async function openFieldTypeMenu() {
  fieldTypeMenuOpen.value = true
  await nextTick()
  updateFieldTypeMenuPosition()
  fieldTypeMenu.value?.querySelector('[role="option"]')?.focus()
}

function toggleFieldTypeMenu() {
  if (fieldTypeMenuOpen.value) closeFieldTypeMenu()
  else openFieldTypeMenu()
}

function closeFieldTypeMenu(returnFocus = false) {
  fieldTypeMenuOpen.value = false
  if (returnFocus) nextTick(() => fieldTypeTrigger.value?.focus())
}

function selectFieldType(type) {
  newFieldType.value = type
  closeFieldTypeMenu()
  fieldTypeTrigger.value?.focus()
}

function handleFieldTypeOutsideClick(event) {
  if (!fieldTypeMenuOpen.value) return
  if (fieldTypeMenu.value?.contains(event.target) || fieldTypeTrigger.value?.contains(event.target)) return
  closeFieldTypeMenu()
}

function handleFieldTypeEscape(event) {
  if (event.key === 'Escape' && fieldTypeMenuOpen.value) closeFieldTypeMenu(true)
}

function openUnlockDialog() {
  unlockPassword.value = ''
  unlockError.value = ''
  unlockDialogOpen.value = true
}

function closeUnlockDialog() {
  unlockDialogOpen.value = false
  unlockPassword.value = ''
  unlockError.value = ''
}

function unlockEditing() {
  if (unlockPassword.value !== configuredEditPassword) {
    unlockError.value = 'That edit password is not correct. Please try again.'
    return
  }
  editUnlocked.value = true
  closeUnlockDialog()
}

function lockEditing() {
  editUnlocked.value = false
  if (nameDialog.kind.startsWith('rename-')) closeNameDialog()
  if (fieldEditor.id) closeFieldEditor()
  noticeMessage.value = 'Editing and delete actions are locked.'
}

function handleViewportChange(event) {
  isMobile.value = event.matches
  sidebarOpen.value = !event.matches
}

function openNameDialog(kind, item = null) {
  if (kind.startsWith('rename-') && !editUnlocked.value) return
  errorMessage.value = ''
  nameDialog.kind = kind
  nameDialog.id = item?.id || ''
  nameDialog.value = item?.name || ''
  nameDialog.open = true
}

function closeNameDialog() {
  nameDialog.open = false
  nameDialog.kind = ''
  nameDialog.id = ''
  nameDialog.value = ''
}

async function submitNameDialog() {
  if (nameDialog.kind.startsWith('rename-') && !editUnlocked.value) {
    closeNameDialog()
    return
  }
  const name = nameDialog.value.trim()
  if (!name) return
  savingName.value = true
  errorMessage.value = ''
  try {
    if (nameDialog.kind === 'create-tab') {
      const newTab = doc(collection(db, 'tabs'))
      await setDoc(newTab, { name, createdAt: serverTimestamp(), updatedAt: serverTimestamp() })
      selectedTabId.value = newTab.id
      noticeMessage.value = 'Tab created.'
    } else if (nameDialog.kind === 'rename-tab') {
      await setDoc(doc(db, 'tabs', nameDialog.id), { name, updatedAt: serverTimestamp() }, { merge: true })
      noticeMessage.value = 'Tab renamed.'
    } else if (nameDialog.kind === 'create-frame') {
      const tabId = selectedTabId.value
      const newFrame = doc(collection(db, 'tabs', tabId, 'frames'))
      await setDoc(newFrame, { name, createdAt: serverTimestamp(), updatedAt: serverTimestamp() })
      selectedFrameId.value = newFrame.id
      noticeMessage.value = 'Frame created.'
    } else if (nameDialog.kind === 'rename-frame') {
      await setDoc(doc(db, 'tabs', selectedTabId.value, 'frames', nameDialog.id), { name, updatedAt: serverTimestamp() }, { merge: true })
      noticeMessage.value = 'Frame renamed.'
    }
    closeNameDialog()
  } catch (error) {
    reportError(error, 'Could not save name')
  } finally {
    savingName.value = false
  }
}

async function deleteDocumentsInChunks(references) {
  for (let start = 0; start < references.length; start += 450) {
    const batch = writeBatch(db)
    references.slice(start, start + 450).forEach(reference => batch.delete(reference))
    await batch.commit()
  }
}

async function deleteTab(tab) {
  if (!editUnlocked.value) return
  if (!window.confirm(`Delete "${tab.name}" and all its frames, fields, and images? This cannot be undone.`)) return
  errorMessage.value = ''
  try {
    const tabPath = ['tabs', tab.id]
    const frameSnapshot = await getDocs(collection(db, ...tabPath, 'frames'))
    const refs = []
    const imageSnapshot = await getDocs(collection(db, ...tabPath, 'images'))
    imageSnapshot.docs.forEach(image => refs.push(image.ref))
    for (const frame of frameSnapshot.docs) {
      const fieldsSnapshot = await getDocs(collection(db, ...tabPath, 'frames', frame.id, 'fields'))
      fieldsSnapshot.docs.forEach(field => refs.push(field.ref))
      refs.push(frame.ref)
    }
    refs.push(doc(db, ...tabPath))
    await deleteDocumentsInChunks(refs)
    if (selectedTabId.value === tab.id) selectedTabId.value = ''
    noticeMessage.value = 'Tab and its content deleted.'
  } catch (error) {
    reportError(error, 'Could not delete tab')
  }
}

async function deleteFrame(frame) {
  if (!editUnlocked.value) return
  if (!window.confirm(`Delete frame "${frame.name}" and all of its fields?`)) return
  errorMessage.value = ''
  try {
    const frameRef = doc(db, 'tabs', selectedTabId.value, 'frames', frame.id)
    const fieldSnapshot = await getDocs(collection(db, 'tabs', selectedTabId.value, 'frames', frame.id, 'fields'))
    const imageSnapshot = await getDocs(collection(db, 'tabs', selectedTabId.value, 'images'))
    const usedImageIds = new Set(fieldSnapshot.docs.flatMap(field => field.data().imageIds || []))
    const refs = fieldSnapshot.docs.map(field => field.ref)
    imageSnapshot.docs.forEach(image => {
      if (usedImageIds.has(image.id)) refs.push(image.ref)
    })
    refs.push(frameRef)
    await deleteDocumentsInChunks(refs)
    noticeMessage.value = 'Frame and its fields deleted.'
  } catch (error) {
    reportError(error, 'Could not delete frame')
  }
}

function fieldTypeLabel(type) {
  return { direct: 'Direct field', keyValue: 'Key–value field', textImages: 'Text and images' }[type] || 'Field'
}

function fieldIcon(type) {
  return { direct: 'Aa', keyValue: '↔', textImages: '▧' }[type] || '•'
}

function openFieldEditor(field = null) {
  if (!selectedTabId.value || !selectedFrameId.value) return
  if (field && !editUnlocked.value) return
  editorError.value = ''
  fieldEditor.id = field?.id || ''
  fieldEditor.type = field?.type || newFieldType.value
  fieldEditor.label = field?.label || ''
  fieldEditor.value = field?.value || ''
  fieldEditor.pairs = field?.pairs?.length ? field.pairs.map(pair => ({ key: pair.key, value: pair.value })) : [{ key: '', value: '' }]
  fieldEditor.text = field?.text || ''
  fieldEditor.images = field?.images?.map(image => ({ ...image, file: null })) || []
  fieldEditor.originalImageIds = field?.imageIds ? [...field.imageIds] : []
  fieldEditor.open = true
}

function closeFieldEditor() {
  fieldEditor.open = false
  fieldEditor.id = ''
  fieldEditor.images = []
  fieldEditor.originalImageIds = []
  editorError.value = ''
}

function addPair() {
  fieldEditor.pairs.push({ key: '', value: '' })
}

function removePair(index) {
  fieldEditor.pairs.splice(index, 1)
  if (fieldEditor.pairs.length === 0) addPair()
}

function validateImage(file) {
  if (!file.type.startsWith('image/')) {
    editorError.value = `${file.name} is not an image file.`
    return false
  }
  if (file.size > MAX_IMAGE_BYTES) {
    editorError.value = `${file.name} exceeds the 650 KiB per-image limit.`
    return false
  }
  return true
}

function previewFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(String(reader.result))
    reader.onerror = () => reject(new Error(`Could not read ${file.name}.`))
    reader.readAsDataURL(file)
  })
}

async function addImages(event) {
  editorError.value = ''
  const files = Array.from(event.target.files || [])
  event.target.value = ''
  for (const file of files) {
    if (fieldEditor.images.length >= MAX_IMAGES) {
      editorError.value = 'A text and images field can contain up to 10 images.'
      break
    }
    if (!validateImage(file)) continue
    try {
      const url = await previewFile(file)
      fieldEditor.images.push({ id: '', name: file.name, url, file })
    } catch (error) {
      editorError.value = error.message
    }
  }
}

async function replaceImage(index, event) {
  editorError.value = ''
  const file = event.target.files?.[0]
  event.target.value = ''
  if (!file || !validateImage(file)) return
  try {
    const url = await previewFile(file)
    fieldEditor.images.splice(index, 1, { id: '', name: file.name, url, file })
  } catch (error) {
    editorError.value = error.message
  }
}

function removeImage(index) {
  fieldEditor.images.splice(index, 1)
}

function fileToBase64(file) {
  return previewFile(file).then(dataUrl => dataUrl.slice(dataUrl.indexOf(',') + 1))
}

async function saveField() {
  if (fieldEditor.id && !editUnlocked.value) {
    closeFieldEditor()
    return
  }
  editorError.value = ''
  if (!fieldEditor.label.trim()) {
    editorError.value = 'Enter a field name.'
    return
  }
  const pairs = fieldEditor.pairs
    .map(pair => ({ key: pair.key.trim(), value: pair.value.trim() }))
    .filter(pair => pair.key || pair.value)
  if (fieldEditor.type === 'keyValue' && (!pairs.length || pairs.some(pair => !pair.key || !pair.value))) {
    editorError.value = 'Complete both the key and value for each pair, or remove the empty pair.'
    return
  }
  if (fieldEditor.type === 'textImages' && fieldEditor.images.length > MAX_IMAGES) {
    editorError.value = 'A text and images field can contain up to 10 images.'
    return
  }
  savingField.value = true
  const isEditing = Boolean(fieldEditor.id)
  try {
    const tabId = selectedTabId.value
    const frameId = selectedFrameId.value
    const fieldId = fieldEditor.id || doc(collection(db, 'tabs', tabId, 'frames', frameId, 'fields')).id
    const batch = writeBatch(db)
    const imageIds = []
    for (const image of fieldEditor.images) {
      if (image.file) {
        const imageRef = doc(collection(db, 'tabs', tabId, 'images'))
        const data = await fileToBase64(image.file)
        batch.set(imageRef, {
          data,
          name: image.name,
          contentType: image.file.type || 'application/octet-stream',
          frameId,
          fieldId,
          createdAt: serverTimestamp()
        })
        imageIds.push(imageRef.id)
      } else if (image.id) {
        imageIds.push(image.id)
      }
    }
    const fieldData = {
      type: fieldEditor.type,
      label: fieldEditor.label.trim(),
      value: fieldEditor.type === 'direct' ? fieldEditor.value.trim() : '',
      pairs: fieldEditor.type === 'keyValue' ? pairs : [],
      text: fieldEditor.type === 'textImages' ? fieldEditor.text.trim() : '',
      imageIds: fieldEditor.type === 'textImages' ? imageIds : [],
      updatedAt: serverTimestamp()
    }
    if (!fieldEditor.id) fieldData.createdAt = serverTimestamp()
    batch.set(doc(db, 'tabs', tabId, 'frames', frameId, 'fields', fieldId), fieldData, { merge: true })

    const retainedIds = new Set(imageIds)
    fieldEditor.originalImageIds.forEach(id => {
      if (!retainedIds.has(id)) batch.delete(doc(db, 'tabs', tabId, 'images', id))
    })
    await batch.commit()
    closeFieldEditor()
    noticeMessage.value = isEditing ? 'Field updated.' : 'Field created.'
  } catch (error) {
    editorError.value = `Could not save field: ${error.message || 'Please try again.'}`
  } finally {
    savingField.value = false
  }
}

async function deleteField(field) {
  if (!editUnlocked.value) return
  if (!window.confirm(`Delete field "${field.label}" and its images?`)) return
  try {
    const batch = writeBatch(db)
    batch.delete(doc(db, 'tabs', selectedTabId.value, 'frames', selectedFrameId.value, 'fields', field.id))
    ;(field.imageIds || []).forEach(id => batch.delete(doc(db, 'tabs', selectedTabId.value, 'images', id)))
    await batch.commit()
    noticeMessage.value = 'Field deleted.'
  } catch (error) {
    reportError(error, 'Could not delete field')
  }
}

function openImage(image) {
  zoomedImage.value = image
}

function closeImage() {
  zoomedImage.value = null
}

onMounted(() => {
  document.addEventListener('pointerdown', handleFieldTypeOutsideClick)
  document.addEventListener('keydown', handleFieldTypeEscape)
  document.addEventListener('scroll', updateFieldTypeMenuPosition, true)
  window.addEventListener('resize', updateFieldTypeMenuPosition)
  mobileQuery.value = window.matchMedia('(max-width: 760px)')
  isMobile.value = mobileQuery.value.matches
  sidebarOpen.value = !isMobile.value
  if (mobileQuery.value.addEventListener) mobileQuery.value.addEventListener('change', handleViewportChange)
  else mobileQuery.value.addListener(handleViewportChange)
  document.addEventListener('visibilitychange', handleVisibilityChange)
  if (isAuthenticated.value) scheduleLogout()
})

onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', handleFieldTypeOutsideClick)
  document.removeEventListener('keydown', handleFieldTypeEscape)
  document.removeEventListener('scroll', updateFieldTypeMenuPosition, true)
  window.removeEventListener('resize', updateFieldTypeMenuPosition)
  clearLoginTimer()
  stopListeners()
  revokeImageUrls()
  document.removeEventListener('visibilitychange', handleVisibilityChange)
  if (mobileQuery.value?.removeEventListener) mobileQuery.value.removeEventListener('change', handleViewportChange)
  else mobileQuery.value?.removeListener(handleViewportChange)
})
</script>

<style>
:root {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #202b3c;
  background: #f5f7fb;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  --ink: #202b3c;
  --muted: #788396;
  --line: #e7ebf2;
  --primary: #5667e9;
  --primary-dark: #4354d4;
  --surface: #ffffff;
}

* { box-sizing: border-box; }
body { margin: 0; min-width: 320px; min-height: 100vh; }
button, input, textarea, select { font: inherit; }
button { cursor: pointer; }
button:disabled { cursor: not-allowed; opacity: .62; }
a { color: inherit; }
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.app-shell { display: flex; min-height: 100vh; overflow: hidden; }
.sidebar {
  z-index: 20;
  display: flex;
  flex: 0 0 278px;
  flex-direction: column;
  width: 278px;
  min-height: 100vh;
  background: #fff;
  border-right: 1px solid var(--line);
  transition: width .24s ease, flex-basis .24s ease, transform .24s ease;
}
.sidebar-is-closed .sidebar { flex-basis: 0; width: 0; overflow: hidden; border-right: 0; }
.sidebar-heading { display: flex; align-items: center; justify-content: space-between; height: 76px; padding: 0 22px; border-bottom: 1px solid #f0f2f6; }
.brand { display: inline-flex; align-items: center; gap: 11px; text-decoration: none; white-space: nowrap; }
.brand-mark { display: grid; width: 38px; height: 38px; flex: 0 0 auto; place-items: center; border-radius: 11px; background: linear-gradient(140deg, #6f7df1, #4d5edb); color: #fff; font-size: 12px; font-weight: 800; letter-spacing: -.3px; box-shadow: 0 5px 12px #5667e930; }
.brand-name { color: #263248; font-size: 16px; font-weight: 750; letter-spacing: -.3px; }
.sidebar-section-heading { display: flex; align-items: center; justify-content: space-between; padding: 25px 18px 10px 24px; color: #98a1b1; font-size: 10px; font-weight: 750; letter-spacing: 1.15px; }
.navigation-tree { flex: 1; min-height: 0; overflow: auto; padding: 0 12px 20px; }
.tree-group { margin: 3px 0; }
.tree-row { display: flex; min-height: 40px; align-items: center; border-radius: 8px; color: #526074; }
.tree-row:hover, .tree-row-active { background: #f1f3ff; color: #4658d8; }
.tree-select { display: flex; flex: 1; min-width: 0; height: 40px; align-items: center; gap: 9px; padding: 0 8px; border: 0; background: transparent; color: inherit; text-align: left; }
.tree-chevron { width: 14px; color: #8d97a7; text-align: center; font-size: 17px; }
.tree-label { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 13px; font-weight: 580; }
.tree-actions { display: flex; align-items: center; padding-right: 4px; opacity: 0; transition: opacity .12s; }
.tree-row:hover .tree-actions, .tree-row:focus-within .tree-actions { opacity: 1; }
.tree-children { margin: 3px 0 8px 18px; padding-left: 8px; border-left: 1px solid #e5e8f0; }
.frame-row .tree-select { height: 36px; }
.frame-indicator { width: 6px; height: 6px; flex: 0 0 auto; border-radius: 50%; background: #c5cbd6; }
.tree-row-active .frame-indicator { background: var(--primary); }
.tree-add-frame { display: flex; height: 34px; align-items: center; gap: 8px; padding: 0 9px; border: 0; background: transparent; color: #828da0; font-size: 12px; }
.tree-add-frame span { font-size: 18px; }
.tree-add-frame:hover, .text-button:hover { color: var(--primary-dark); }
.tree-empty { display: grid; gap: 8px; padding: 14px 12px; color: #8993a3; font-size: 12px; }
.sidebar-footer { display: flex; align-items: center; gap: 10px; padding: 14px 16px; border-top: 1px solid var(--line); }
.account-avatar { display: grid; width: 34px; height: 34px; flex: 0 0 auto; place-items: center; border-radius: 50%; background: #e8ebff; color: #4b5cda; font-size: 9px; font-weight: 800; letter-spacing: -.25px; }
.account-label { flex: 1; color: #5b6678; font-size: 12px; }

.main-area { display: flex; min-width: 0; flex: 1; flex-direction: column; height: 100vh; }
.topbar { z-index: 5; display: flex; height: 64px; flex: 0 0 64px; align-items: center; gap: 16px; padding: 0 34px; border-bottom: 1px solid var(--line); background: rgba(255,255,255,.92); }
.topbar-spacer { flex: 1; }
.menu-toggle { display: inline-flex; align-items: center; gap: 9px; padding: 8px 10px; border: 0; border-radius: 8px; background: transparent; color: #5e6a7d; font-size: 12px; font-weight: 650; }
.menu-toggle:hover { background: #f0f2f8; color: var(--primary-dark); }
.menu-toggle span:first-child { font-size: 19px; line-height: 12px; }
.session-indicator { display: flex; align-items: center; gap: 7px; color: #7d8798; font-size: 11px; white-space: nowrap; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; background: #4ab783; }
.edit-lock-button { display: inline-flex; min-height: 34px; align-items: center; gap: 7px; padding: 0 10px; border: 1px solid #e4e8ef; border-radius: 8px; background: #fff; color: #6f7989; font-size: 11px; font-weight: 650; white-space: nowrap; }
.edit-lock-button > span:first-child { font-size: 13px; }
.edit-lock-button:hover { border-color: #cfd5e0; background: #f8f9fc; }
.edit-lock-button.edit-lock-open { border-color: #d3eadc; background: #f3fbf6; color: #397953; }
.content-scroll { width: 100%; max-width: 1200px; flex: 1; overflow: auto; margin: 0 auto; padding: 40px clamp(20px, 5vw, 64px) 60px; }
.page-heading { display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; margin-bottom: 30px; }
.page-heading h1, .welcome-panel h1 { margin: 5px 0 8px; color: #202b3c; font-size: clamp(26px, 3vw, 34px); letter-spacing: -1.1px; }
.breadcrumb { margin: 0; color: #8a94a5; font-size: 12px; }
.muted { color: var(--muted); line-height: 1.65; }
.page-heading .muted { margin: 0; font-size: 13px; }
.eyebrow { margin: 0 0 8px; color: #8b95a7; font-size: 10px; font-weight: 750; letter-spacing: 1.15px; }
.button { display: inline-flex; min-height: 40px; align-items: center; justify-content: center; gap: 8px; padding: 0 15px; border: 1px solid transparent; border-radius: 9px; font-size: 12px; font-weight: 680; transition: background .15s, border-color .15s, color .15s; }
.button-primary { background: var(--primary); color: white; box-shadow: 0 4px 10px #5667e922; }
.button-primary:hover { background: var(--primary-dark); }
.button-subtle { border-color: #e2e6ee; background: #fff; color: #566174; }
.button-subtle:hover { border-color: #cdd3e0; background: #f8f9fc; }
.button-danger { border-color: #f2dede; background: #fff; color: #bd5b5b; }
.button-danger:hover { background: #fff4f4; }
.button-small { min-height: 30px; padding: 0 10px; border-radius: 7px; font-size: 11px; }
.button-wide { width: 100%; }
.button-disabled { opacity: .55; cursor: not-allowed; }
.card { border: 1px solid #e9edf4; border-radius: 14px; background: #fff; box-shadow: 0 5px 20px #263b5608; }
.add-field-panel { display: flex; align-items: center; justify-content: space-between; gap: 20px; padding: 22px 24px; }
.add-field-panel h2, .fields-heading h2 { margin: 0; color: #2a3547; font-size: 16px; letter-spacing: -.25px; }
.add-field-panel .muted { margin: 5px 0 0; font-size: 12px; }
.add-field-panel strong { color: #536077; font-weight: 650; }
.field-create-control { display: flex; flex: 0 0 auto; gap: 9px; }
select, input[type="text"], input[type="password"], textarea, .pair-editor input { min-width: 0; border: 1px solid #dfe4ed; border-radius: 8px; outline: none; background: #fff; color: #2c3748; }
select:focus, input:focus, textarea:focus { border-color: #8792ed; box-shadow: 0 0 0 3px #6677e91a; }
.field-type-trigger { display: flex; min-width: 200px; min-height: 40px; align-items: center; justify-content: space-between; gap: 12px; padding: 0 12px; border: 1px solid #dfe4ed; border-radius: 8px; background: #fff; color: #2c3748; font-size: 12px; text-align: left; }
.field-type-trigger:hover { border-color: #bfc7d8; }
.field-type-trigger:focus-visible, .field-type-option:focus-visible { outline: 3px solid #6677e955; outline-offset: 2px; }
.field-type-menu { position: fixed; z-index: 10000; overflow-x: hidden; overflow-y: auto; padding: 6px; border: 1px solid #e1e6ef; border-radius: 11px; background: #fff; box-shadow: 0 16px 38px #1e2b4430; }
.field-type-option { display: flex; width: 100%; min-height: 44px; align-items: center; gap: 10px; padding: 0 10px; border: 0; border-radius: 7px; background: transparent; color: #425067; font-size: 12px; text-align: left; }
.field-type-option:hover, .field-type-option-active { background: #f0f2ff; color: #4e5fd8; }
.field-type-option-icon { display: grid; width: 27px; height: 27px; flex: 0 0 auto; place-items: center; border-radius: 8px; background: #e9ecff; color: #5667d8; font-size: 11px; font-weight: 750; }
.field-type-check { margin-left: auto; color: #5667d8; }
.fields-heading { display: flex; align-items: center; justify-content: space-between; margin: 32px 1px 14px; }
.fields-heading > div { display: flex; align-items: center; gap: 9px; }
.count-pill { display: inline-grid; min-width: 22px; height: 22px; place-items: center; padding: 0 6px; border-radius: 11px; background: #e9ecff; color: #5667d8; font-size: 10px; font-weight: 750; }
.small-text { font-size: 11px; }
.field-list { display: grid; gap: 14px; }
.field-card { overflow: hidden; padding: 20px 22px; }
.field-card-header { display: flex; min-width: 0; align-items: center; justify-content: space-between; gap: 16px; padding-bottom: 15px; border-bottom: 1px solid #f0f2f6; }
.field-title-group { display: flex; min-width: 0; align-items: center; gap: 12px; }
.field-type-icon { display: grid; width: 38px; height: 38px; flex: 0 0 auto; place-items: center; border-radius: 11px; background: #eef0ff; color: #5b6be0; font-size: 13px; font-weight: 750; }
.field-type-label { margin: 0 0 3px; color: #969faf; font-size: 10px; }
.field-card h3 { overflow-wrap: anywhere; margin: 0; color: #273448; font-size: 14px; }
.field-card-actions { display: flex; flex: 0 0 auto; gap: 7px; }
.field-body { margin: 16px 0 0; color: #505d70; font-size: 13px; line-height: 1.75; }
.direct-value { white-space: pre-wrap; overflow-wrap: anywhere; }
.key-value-list { display: grid; min-width: 0; grid-template-columns: minmax(0, min(32%, 180px)) minmax(0, 1fr); gap: 9px 18px; margin: 17px 0 0; font-size: 12px; }
.key-value-list dt { color: #8a94a5; }
.key-value-list dd { min-width: 0; margin: 0; color: #435064; overflow-wrap: anywhere; }
.key-value-list p { grid-column: 1 / -1; margin: 0; }
.text-image-content > p { margin: 16px 0; }
.preserve-lines { white-space: pre-wrap; overflow-wrap: anywhere; }
.image-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(112px, 1fr)); gap: 10px; margin-top: 14px; }
.image-thumbnail { overflow: hidden; aspect-ratio: 1; padding: 0; border: 1px solid #e9edf4; border-radius: 10px; background: #f6f7fa; }
.image-thumbnail img { width: 100%; height: 100%; object-fit: cover; transition: transform .18s; }
.image-thumbnail:hover img { transform: scale(1.04); }
.image-count { margin: 8px 0 0 !important; color: #97a0af; font-size: 10px; }
.empty-fields, .empty-state { padding: 40px 24px; text-align: center; }
.empty-fields h3, .empty-state h2 { margin: 13px 0 7px; color: #334054; font-size: 15px; }
.empty-fields .muted, .empty-state .muted { max-width: 460px; margin: 0 auto 18px; font-size: 12px; }
.empty-state-icon, .welcome-icon { display: grid; width: 48px; height: 48px; place-items: center; margin: 0 auto; border-radius: 15px; background: #eef0ff; color: #5869e4; font-size: 22px; }
.welcome-panel { max-width: 580px; margin: clamp(50px, 15vh, 150px) auto; text-align: center; }
.welcome-icon { width: 58px; height: 58px; margin-bottom: 24px; font-size: 26px; }
.welcome-panel .eyebrow { margin-bottom: 10px; }
.welcome-panel .muted { margin: 0 auto 22px; font-size: 14px; }

.icon-button { display: inline-grid; width: 30px; height: 30px; flex: 0 0 auto; place-items: center; padding: 0; border: 0; border-radius: 7px; background: transparent; color: #8b95a4; font-size: 18px; line-height: 1; }
.icon-button:hover { background: #eef0f6; color: #526071; }
.icon-button.compact { width: 24px; height: 25px; font-size: 14px; }
.danger-on-hover:hover { background: #fff0f0; color: #c15656; }
.text-button { padding: 0; border: 0; background: transparent; color: #6372de; font-size: 11px; font-weight: 650; }
.text-danger { color: #bc6060; }
.sidebar-close { display: none; }
.alert { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 18px; padding: 11px 14px; border: 1px solid; border-radius: 9px; font-size: 12px; }
.alert-error { border-color: #f2d1d1; background: #fff5f5; color: #a64444; }
.alert-success { border-color: #d3eadc; background: #f3fbf6; color: #397953; }

.modal-backdrop { position: fixed; z-index: 50; inset: 0; display: grid; place-items: center; overflow: auto; padding: 20px; background: #17203380; backdrop-filter: blur(3px); }
.modal-card { position: relative; width: min(100%, 440px); max-height: calc(100dvh - 40px); overflow: auto; padding: 30px; border: 1px solid #e9edf4; border-radius: 18px; background: #fff; box-shadow: 0 24px 70px #15233a35; }
.modal-card h2 { margin: 0 0 21px; color: #273448; font-size: 22px; letter-spacing: -.55px; }
.unlock-description { margin: -12px 0 18px; font-size: 12px; }
.modal-close { position: absolute; top: 16px; right: 16px; }
.modal-form { display: grid; gap: 9px; }
.modal-form > label { margin-top: 7px; color: #556174; font-size: 11px; font-weight: 650; }
.modal-form input[type="text"], .modal-form textarea { width: 100%; padding: 11px 12px; font-size: 12px; }
.modal-form textarea { resize: vertical; line-height: 1.6; }
.modal-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 17px; }
.field-editor { width: min(100%, 650px); }
.editor-form { gap: 10px; }
.subform-heading { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: 7px; }
.subform-heading > div > label { color: #556174; font-size: 11px; font-weight: 650; }
.subform-heading p { margin: 4px 0 0; }
.pair-editor { display: grid; grid-template-columns: 1fr 1fr 30px; gap: 8px; }
.pair-editor > * { min-width: 0; }
.pair-editor input { width: 100%; padding: 10px; font-size: 12px; }
.image-upload-heading { margin-top: 6px; }
.file-picker { position: relative; overflow: hidden; cursor: pointer; }
.file-picker input, .replace-picker input { position: absolute; width: 1px; height: 1px; overflow: hidden; opacity: 0; }
.editor-image-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; }
.editor-image { overflow: hidden; border: 1px solid var(--line); border-radius: 10px; }
.editor-image-preview { display: block; width: 100%; height: 120px; padding: 0; border: 0; background: #f3f5f8; }
.editor-image-preview img { width: 100%; height: 100%; object-fit: cover; }
.editor-image-actions { display: flex; align-items: center; gap: 9px; padding: 8px; }
.image-name { min-width: 0; flex: 1; overflow: hidden; color: #748093; font-size: 9px; text-overflow: ellipsis; white-space: nowrap; }
.replace-picker { position: relative; cursor: pointer; }
.form-error { margin: 4px 0 0; color: #b24646; font-size: 11px; line-height: 1.5; }
.editor-actions { position: sticky; bottom: -30px; padding: 14px 0 2px; background: white; }
.image-viewer-backdrop { z-index: 60; background: #101725e8; }
.image-viewer { position: relative; display: flex; max-width: min(94vw, 1200px); max-height: 92dvh; flex-direction: column; align-items: center; }
.image-viewer img { display: block; max-width: 100%; max-height: 84dvh; border-radius: 7px; object-fit: contain; }
.viewer-close { position: fixed; top: 16px; right: 20px; width: 42px; height: 42px; background: #ffffff20; color: white; font-size: 28px; }
.viewer-close:hover { background: #ffffff36; color: #fff; }
.viewer-caption { margin: 9px 0 0; color: #fff; font-size: 12px; }

.login-page { display: grid; min-height: 100vh; place-items: center; padding: 24px; background: radial-gradient(ellipse at 50% 20%, #edf0ff 0, #f5f7fb 54%, #f8f9fc 100%); }
.login-card { position: relative; width: min(100%, 410px); padding: 42px; border: 1px solid #e8ebf3; border-radius: 20px; background: #fff; box-shadow: 0 22px 70px #283a5b12; }
.brand-mark-large { width: 52px; height: 52px; margin-bottom: 27px; border-radius: 15px; font-size: 16px; }
.theme-toggle { display: inline-flex; min-height: 34px; align-items: center; justify-content: center; gap: 7px; padding: 0 10px; border: 1px solid #e2e6ee; border-radius: 8px; background: #fff; color: #586477; font-size: 11px; font-weight: 650; white-space: nowrap; }
.theme-toggle:hover { border-color: #cdd3e0; background: #f8f9fc; }
.theme-toggle > span:first-child { font-size: 14px; }
.login-theme-toggle { position: absolute; top: 16px; right: 16px; }
.login-card h1 { margin: 0 0 9px; color: #202b3c; font-size: 28px; letter-spacing: -.8px; }
.login-card > .muted { margin: 0; font-size: 12px; }
.login-form { display: grid; gap: 9px; margin-top: 27px; }
.login-form label { color: #526074; font-size: 11px; font-weight: 650; }
.login-form input { width: 100%; height: 43px; padding: 0 12px; }
.login-footnote { margin: 21px 0 0; color: #9aa3b1; font-size: 10px; text-align: center; }

.sidebar-backdrop { display: none; }
.field-create-control > *, .modal-form > input, .modal-form > textarea { min-width: 0; max-width: 100%; }

.theme-dark {
  color-scheme: dark;
  --ink: #e8edf5;
  --muted: #a1adbf;
  --line: #313b4c;
  --surface: #1c2532;
  color: #e8edf5;
}
:root[data-theme="dark"] { background: #101620; color: #e8edf5; }
.theme-dark.login-page { background: radial-gradient(ellipse at 50% 20%, #232b40 0, #141b27 56%, #101620 100%); }
.theme-dark.app-shell { background: #141b26; }
.theme-dark .sidebar,
.theme-dark .topbar,
.theme-dark .card,
.theme-dark .modal-card,
.theme-dark .login-card,
.theme-dark .field-type-trigger,
.theme-dark .theme-toggle { border-color: #303b4d; background-color: #1c2532; color: #e3e9f2; }
.theme-dark .sidebar-heading,
.theme-dark .sidebar-footer,
.theme-dark .field-card-header { border-color: #303b4d; }
.theme-dark .brand-name,
.theme-dark .page-heading h1,
.theme-dark .welcome-panel h1,
.theme-dark .add-field-panel h2,
.theme-dark .fields-heading h2,
.theme-dark .field-card h3,
.theme-dark .empty-fields h3,
.theme-dark .empty-state h2,
.theme-dark .modal-card h2,
.theme-dark .login-card h1 { color: #e8edf5; }
.theme-dark .tree-row { color: #aab5c5; }
.theme-dark .tree-row:hover,
.theme-dark .tree-row-active { background: #293149; color: #c7ceff; }
.theme-dark .tree-add-frame,
.theme-dark .tree-empty,
.theme-dark .sidebar-section-heading,
.theme-dark .eyebrow,
.theme-dark .account-label,
.theme-dark .breadcrumb,
.theme-dark .muted,
.theme-dark .field-type-label,
.theme-dark .key-value-list dt,
.theme-dark .field-body,
.theme-dark .direct-value { color: #a5b0c1; }
.theme-dark .account-avatar,
.theme-dark .field-type-icon,
.theme-dark .field-type-option-icon,
.theme-dark .count-pill,
.theme-dark .empty-state-icon,
.theme-dark .welcome-icon { background: #303a58; color: #c1c9ff; }
.theme-dark .button-subtle,
.theme-dark .button-danger,
.theme-dark .icon-button,
.theme-dark .menu-toggle,
.theme-dark .edit-lock-button { border-color: #3a4659; background: #222c3a; color: #d3dbe7; }
.theme-dark .button-subtle:hover,
.theme-dark .icon-button:hover,
.theme-dark .menu-toggle:hover,
.theme-dark .theme-toggle:hover { background: #2c3748; }
.theme-dark .button-danger { border-color: #5a3d48; color: #f0aaaa; }
.theme-dark .button-danger:hover,
.theme-dark .danger-on-hover:hover { background: #4a2e3a; color: #ffb8b8; }
.theme-dark .edit-lock-button.edit-lock-open { border-color: #365747; background: #20382e; color: #9cdbb5; }
.theme-dark .field-type-trigger,
.theme-dark .modal-form input[type="text"],
.theme-dark .modal-form input[type="password"],
.theme-dark .modal-form textarea,
.theme-dark .pair-editor input,
.theme-dark .login-form input { border-color: #3b475a; background: #151d29; color: #e4eaf3; }
.theme-dark .field-type-menu { border-color: #364255; background: #202a38; box-shadow: 0 16px 38px #0008; }
.theme-dark .field-type-option { color: #d1d9e6; }
.theme-dark .field-type-option:hover,
.theme-dark .field-type-option-active { background: #313b56; color: #d5daff; }
.theme-dark .field-type-check { color: #b6c0ff; }
.theme-dark .key-value-list dd { color: #d0d8e5; }
.theme-dark .image-thumbnail,
.theme-dark .editor-image { border-color: #364255; background: #151d29; }
.theme-dark .editor-image-preview { background: #121923; }
.theme-dark .editor-actions { background: #1c2532; }
.theme-dark .modal-close { background: transparent; }
.theme-dark .modal-close:hover { background: #303b4c; }
.theme-dark .alert-error { border-color: #63434a; background: #38272e; color: #ffc0c0; }
.theme-dark .alert-success { border-color: #345746; background: #20362e; color: #b0e1c1; }
.theme-dark .form-error { color: #ffaaaa; }
.theme-dark .login-footnote,
.theme-dark .login-form label { color: #a5b0c1; }
.theme-dark .modal-form > label,
.theme-dark .subform-heading > div > label { color: #c6d0df; }
.theme-dark .field-create-control .button-primary,
.theme-dark .modal-actions .button-primary,
.theme-dark .login-form .button-primary { border-color: transparent; background: #6373ed; color: #fff; }
.theme-dark .field-create-control .button-primary:hover,
.theme-dark .modal-actions .button-primary:hover,
.theme-dark .login-form .button-primary:hover { background: #7583ff; }
.theme-dark .field-type-trigger:focus-visible,
.theme-dark .field-type-option:focus-visible { outline-color: #8995ff; }
:root[data-theme="dark"] .field-type-menu { border-color: #364255; background: #202a38; box-shadow: 0 16px 38px #0008; }
:root[data-theme="dark"] .field-type-option { color: #d1d9e6; }
:root[data-theme="dark"] .field-type-option:hover,
:root[data-theme="dark"] .field-type-option-active { background: #313b56; color: #d5daff; }
:root[data-theme="dark"] .field-type-option-icon { background: #303a58; color: #c1c9ff; }

@media (max-width: 900px) {
  .sidebar { flex-basis: 250px; width: 250px; }
  .sidebar-is-closed .sidebar { flex-basis: 0; width: 0; }
  .content-scroll { padding-right: 28px; padding-left: 28px; }
  .topbar { padding-right: 24px; padding-left: 24px; }
  .add-field-panel { align-items: stretch; flex-direction: column; }
  .field-create-control { width: 100%; }
  .field-type-trigger { flex: 1; min-width: 0; }
}

@media (max-width: 760px) {
  .sidebar {
    position: fixed;
    inset: 0 auto 0 0;
    width: min(300px, calc(100vw - 54px));
    min-height: 100dvh;
    transform: translateX(0);
    box-shadow: 12px 0 34px #1c2b4517;
  }
  .sidebar-is-closed .sidebar { width: min(300px, calc(100vw - 54px)); transform: translateX(-105%); }
  .sidebar-backdrop { position: fixed; z-index: 19; inset: 0; display: block; border: 0; background: #111b2e70; }
  .sidebar-close { display: inline-grid; }
  .main-area { width: 100%; height: 100dvh; }
  .topbar { height: 58px; flex-basis: 58px; gap: 9px; padding: 0 14px; }
  .menu-toggle { padding: 8px 7px; }
  .session-indicator { font-size: 0; }
  .status-dot { width: 8px; height: 8px; }
  .logout-button { min-height: 34px; padding: 0 9px; font-size: 10px; }
  .content-scroll { padding: 27px 17px 42px; }
  .page-heading { margin-bottom: 23px; }
  .page-heading > .button { display: none; }
  .add-field-panel { padding: 18px; }
  .field-card { min-width: 0; padding: 16px; }
  .field-card-header { align-items: flex-start; flex-wrap: wrap; }
  .field-title-group { min-width: 0; flex: 1 1 160px; }
  .field-card-actions { width: 100%; justify-content: flex-end; }
  .field-card-actions .button { min-height: 38px; }
  .edit-lock-button { min-height: 38px; }
  .key-value-list { column-gap: 12px; }
  .editor-image-actions { flex-wrap: wrap; }
  .image-name { flex-basis: 100%; }
  .tree-actions { opacity: 1; }
}

@media (max-width: 480px) {
  .brand-name { font-size: 14px; }
  .content-scroll { padding-right: 13px; padding-left: 13px; }
  .page-heading h1 { font-size: 26px; }
  .field-create-control { align-items: stretch; flex-direction: column; }
  .field-type-trigger { min-height: 42px; }
  .field-card-header { align-items: flex-start; }
  .field-card-actions { justify-content: stretch; gap: 7px; }
  .field-card-actions .button { min-height: 42px; flex: 1; }
  .button-small { padding: 0 8px; }
  .key-value-list { grid-template-columns: minmax(0, 34%) minmax(0, 1fr); gap: 8px 10px; }
  .modal-backdrop { align-items: end; padding: 0; }
  .modal-card { width: 100%; max-height: min(90dvh, 850px); padding: 25px 20px; border-radius: 18px 18px 0 0; }
  .editor-actions { bottom: -25px; }
  .login-card { padding: 30px 24px; }
  .pair-editor { grid-template-columns: minmax(0, 1fr) 28px; gap: 6px; }
  .pair-editor input:first-child { grid-column: 1; grid-row: 1; }
  .pair-editor input:nth-child(2) { grid-column: 1; grid-row: 2; }
  .pair-editor .icon-button { grid-column: 2; grid-row: 1 / span 2; align-self: center; }
  .pair-editor input { padding: 9px 7px; }
  .image-grid { grid-template-columns: repeat(auto-fill, minmax(85px, 1fr)); }
  .edit-lock-button { width: 38px; justify-content: center; padding: 0; }
  .edit-lock-button > span:last-child { display: none; }
  .topbar { gap: 6px; padding-right: 10px; padding-left: 10px; }
  .menu-toggle { gap: 6px; font-size: 11px; }
  .logout-button { min-height: 36px; }
}

@media (max-width: 360px) {
  .menu-toggle > span:last-child { display: none; }
  .field-card { padding: 13px; }
  .field-card-actions .button { padding: 0 5px; font-size: 10px; }
  .login-page { padding: 14px; }
  .login-card { padding: 26px 20px; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; }
}
</style>
