export interface Organization {
  id: string;
  name: string;
  owner_id: string;
  created_at: string;
}

export interface CreateOrganizationRequest {
  name: string;
}

export interface OrganizationsListResponse {
  organizations: Organization[];
  total: number;
}
