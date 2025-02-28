<template>
  <div class="setting-text">
    <div v-if="input === null || !input.length" class="font-italic text-black-50">
      Empty
    </div>
    <div v-else>
      {{ trimmed(text) }}
    </div>
    <b-modal class="setting-object-modal" v-model="showModal" size="lg" @hidden="onModalHidden" @show="onShowModal">
      <template v-slot:modal-header class="d-block">
        <div>
          <h5 class="mb-0" v-if="setting.name">{{ $t(setting.name) }}</h5>
          <h5 class="mb-0" v-else>{{ setting.key }}</h5>
          <small class="form-text text-muted" v-if="setting.helper">{{ $t(setting.helper) }}</small>
        </div>
        <button type="button" :aria-label="$t('Close')" class="close" @click="onCancel">×</button>
      </template>
      <div v-if="error" class="alert alert-danger">
        {{ $t('Unable to load options.') }}
      </div>
      <div v-else-if="loaded">
        <b-form-group
          :invalid-feedback="$t(message)"
          :state="invalid ? false : null"
        >
          <b-form-checkbox-group
            v-model="transformed"
            :options="options"
            :switches="switches"
            stacked
            @change="onChanged"
          />
        </b-form-group>
      </div>
      <div v-else>
        <i class="fas fa-cog fa-spin text-secondary"></i> {{ $t('Loading...') }}
      </div>
      <div slot="modal-footer" class="w-100 m-0 d-flex">
        <button type="button" class="btn btn-outline-secondary ml-auto" @click="onCancel">
            {{ $t('Cancel') }}
        </button>
        <button type="button" class="btn btn-secondary ml-3" @click="onSave" :disabled="invalid || ! changed">
            {{ $t('Save')}}
        </button>
      </div>
    </b-modal>
  </div>
</template>

<script>
import settingMixin from "../mixins/setting";

export default {
  mixins: [settingMixin],
  props: ['value', 'setting'],
  data() {
    return {
      message: '',
      invalid: false,
      error: false,
      input: null,
      loaded: false,
      options: [],
      selected: null,
      showModal: false,
      transformed: [],
    };
  },
  computed: {
    variant() {
      if (this.disabled) {
        return 'secondary';
      } else {
        return 'success';
      }
    },
    changed() {
      return JSON.stringify(this.input) !== JSON.stringify(this.transformed);
    },
    display() {
      const options = this.ui('options');
      const keys = Object.keys(options);
      if (keys.includes(this.input)) {
        return options[this.input];
      } else {
        return this.input;
      }
    },
    text() {
      if (this.input && this.input.length) {
        return this.input.join(', ');
      } else {
        return '';
      }
    },
    switches() {
      if (this.ui('switches')) {
        return true;
      } else {
        return false;
      }
    },
  },
  watch: {
    value: {
      handler: function(value) {
        this.input = value;
      },
    }
  },
  methods: {
    onChanged() {
      this.invalid = false;
      this.message = '';
    },
    onCancel() {
      this.showModal = false;
    },
    onEdit() {
      this.showModal = true;
    },
    onModalHidden() {
      this.transformed = this.copy(this.input);
      this.error = false;
      if (this.ui('dynamic')) {
        this.loaded = false;
        this.options = [];
      }
      this.invalid = false;
      this.message = '';
    },
    onShowModal() {
      if (! this.loaded && this.ui('dynamic')) {
        let settings = this.ui('dynamic');
        ProcessMaker.apiClient.get(settings.url).then(response => {
          let data = _.get(response, settings.response);
          if (data) {
            this.options = data;
            this.loaded = true;
          }
        }).catch(error => {
          this.error = true;
        });
      }
    },
    async onSave() {
      const testSettingEndpoint = this.ui('testSettingEndpoint');
      const enabled = this.copy(this.transformed);
      if (testSettingEndpoint) {
        try {
          await ProcessMaker.apiClient.post(testSettingEndpoint, { enabled });
        } catch (error) {
          this.invalid = true;
          this.message = error.response.data.message || error.message;
          return;
        }
      }
      this.input = enabled;
      this.showModal = false;
      this.emitSaved(this.input);
    },
  },
  mounted() {
    if (this.value === null) {
      this.input = [];
    } else {
      this.input = this.value;
    }
    if (! this.ui('dynamic')) {
      this.options = this.ui('options');
      this.loaded = true;
    }
    this.transformed = this.copy(this.input);
  }
};
</script>

<style lang="scss" scoped>
  @import '../../../../sass/colors';

  $disabledBackground: lighten($secondary, 20%);

  .btn:disabled,
  .btn.disabled {
    background: $disabledBackground;
    border-color: $disabledBackground;
    opacity: 1 !important;
  }
</style>
