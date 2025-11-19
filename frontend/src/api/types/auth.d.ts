import { useTypes } from '@/composables/useTypes'

export interface UserAuth {
  /**
   *  (1)使用者
   */
  roleId: number
  token: string
}

export interface LoginRequestData {
  email: string
  password: string
}
export interface LoginResponseData {
  /**
   *  (1)使用者
   */
  identity: number
  identifier: string
}

type Identity = 1 | 2 | 3
type Gender = 1 | 2 | 3 | 4
type OrganizationAddType = 1 | 2
//註冊資料
namespace RegisterData {
  /**
   * 取得驗證碼
   */
  type getCode = {
    /**
     * 1 : 輸入身分及email 2 : 確認驗證碼 3 : 輸入個人資料
     */
    action: 1
    /**
     * 1 : 消費者 2 : 業主 3 : 組織
     */
    identity: Identity
  }
  /**
   * 驗證驗證碼
   */
  type verifyCode = {
    /**
     * 1 : 輸入身分及email 2 : 確認驗證碼 3 : 輸入個人資料
     */
    action: 2
    code: string
    /**
     * 1 : 消費者 2 : 業主 3 : 組織
     */
    identity: Identity
  }
  /**
   * 輸入個人資料的資料
   */
  namespace ProfileData {
    type consumer = {
      identity: 1
      /**
       * 1 : 男性 2 : 女性 3 : 其他 4 : 不願透漏
       */
      gender: Gender
    }
    type merchant = {
      /**
       * 1 : 消費者 2 : 業主 3 : 組織
       */
      identity: 2
    }
    type organization = {
      /**
       * 1 : 消費者 2 : 業主 3 : 組織
       */
      identity: 3
      /**
       * 1 : 自由加入 2 : 須審核
       */
      free: OrganizationAddType
      title: string
    }
  }

  type profileData = {
    action: 3

    password: string
    passwordCheck: string
    name: string
  } & (ProfileData.consumer | ProfileData.merchant | ProfileData.organization)
}

export type RegisterRequestData = {
  email: string
} & (RegisterData.getCode | RegisterData.profileData | RegisterData.verifyCode)

export namespace ForgetPasswordData {
  export type action = 1 | 2 | 3
  export interface getCode {
    email: string
  }

  export interface verifyCode extends getCode {
    code: string
  }

  export interface resetPassword extends verifyCode {
    np: string
  }
}
