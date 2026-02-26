export interface TaxBreakdown {
  state_rate: number;
  county_rate: number;
  city_rate: number;
  special_rates: number;
}

export interface Order {
  id?: number;
  longitude: number;
  latitude: number;
  subtotal: number;
  timestamp: string;
  composite_tax_rate?: number;
  tax_amount?: number;
  total_amount?: number;
  breakdown?: TaxBreakdown;
}